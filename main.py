"""Maíz Urbano: aplicación local de escritorio (Python + pywebview + SQLite)."""
from __future__ import annotations
import json
from contextlib import contextmanager
import tempfile
import sqlite3
import sys
from datetime import date, datetime, timedelta
from pathlib import Path

def resolve_paths(*, frozen=None, executable=None, bundle_dir=None, source_file=None):
    """Separate writable portable data from bundled, read-only UI resources.

    PyInstaller --onedir places --add-data contents under sys._MEIPASS
    (normally dist/MaizUrbano/_internal), NOT next to the .exe.
    """
    if frozen is None:
        frozen = bool(getattr(sys, 'frozen', False))
    if frozen:
        executable_dir = Path(executable or sys.executable).resolve().parent
        resources_dir = Path(bundle_dir or getattr(sys, '_MEIPASS', executable_dir / '_internal')).resolve()
        return executable_dir, resources_dir
    project_dir = Path(source_file or __file__).resolve().parent
    return project_dir, project_dir


DATA_ROOT, RESOURCE_ROOT = resolve_paths()
DB_PATH = DATA_ROOT / 'data' / 'maiz_urbano.db'
FRONTEND_PATH = RESOURCE_ROOT / 'frontend' / 'index.html' 

MENU = [
 ('des-cre-g', 'Desgranado grande', 'Desgranados', 55, 'Crema, mayonesa y queso', 'cup'),
 ('des-cre-m', 'Desgranado mediano', 'Desgranados', 45, 'Crema, mayonesa y queso', 'cup'),
 ('des-cre-c', 'Desgranado chico', 'Desgranados', 40, 'Crema, mayonesa y queso', 'cup'),
 ('des-sal-g', 'Desgranado grande', 'Desgranados', 50, 'Sal, limón y chile', 'cup'),
 ('des-sal-m', 'Desgranado mediano', 'Desgranados', 35, 'Sal, limón y chile', 'cup'),
 ('des-sal-c', 'Desgranado chico', 'Desgranados', 30, 'Sal, limón y chile', 'cup'),
 ('el-cre', 'Elote entero', 'Elotes', 35, 'Crema, mayonesa y queso', 'cob'),
 ('el-sal', 'Elote entero', 'Elotes', 25, 'Sal, limón y chile', 'cob'),
 ('tostielote', 'Tostielote', 'Antojitos', 70, 'Con elote', 'tosti'),
 ('papalote', 'Papalote', 'Antojitos', 50, 'Papa con elote', 'potato'),
 ('maruchan', 'Maruchan con elote', 'Antojitos', 85, 'Con elote', 'noodle'),
]

SCHEMA = '''
PRAGMA foreign_keys=ON;
CREATE TABLE IF NOT EXISTS products(id TEXT PRIMARY KEY,name TEXT NOT NULL,category TEXT NOT NULL,price_cents INTEGER NOT NULL,description TEXT,art TEXT);
CREATE TABLE IF NOT EXISTS sales(id INTEGER PRIMARY KEY,created_at TEXT NOT NULL,payment TEXT NOT NULL,total_cents INTEGER NOT NULL);
CREATE TABLE IF NOT EXISTS sale_items(id INTEGER PRIMARY KEY,sale_id INTEGER NOT NULL REFERENCES sales(id),product_id TEXT NOT NULL,product_name TEXT NOT NULL,description TEXT,quantity INTEGER NOT NULL,unit_cents INTEGER NOT NULL);
CREATE TABLE IF NOT EXISTS inventory_items(id INTEGER PRIMARY KEY,name TEXT UNIQUE NOT NULL,unit TEXT NOT NULL,category TEXT NOT NULL);
CREATE TABLE IF NOT EXISTS stock_entries(id INTEGER PRIMARY KEY,item_id INTEGER NOT NULL REFERENCES inventory_items(id),quantity REAL NOT NULL CHECK(quantity>0),created_at TEXT NOT NULL,expires_on TEXT,notes TEXT);
CREATE TABLE IF NOT EXISTS stock_movements(id INTEGER PRIMARY KEY,entry_id INTEGER NOT NULL REFERENCES stock_entries(id),quantity REAL NOT NULL CHECK(quantity<0),kind TEXT NOT NULL,reason TEXT NOT NULL,created_at TEXT NOT NULL);
CREATE TABLE IF NOT EXISTS purchases(id INTEGER PRIMARY KEY,created_at TEXT NOT NULL,concept TEXT NOT NULL,amount_cents INTEGER NOT NULL CHECK(amount_cents>=0),payment TEXT NOT NULL,notes TEXT);
CREATE TABLE IF NOT EXISTS expenses(id INTEGER PRIMARY KEY,created_at TEXT NOT NULL,concept TEXT NOT NULL,amount_cents INTEGER NOT NULL CHECK(amount_cents>=0),payment TEXT NOT NULL,notes TEXT);
CREATE TABLE IF NOT EXISTS cash_sessions(id INTEGER PRIMARY KEY,opened_at TEXT NOT NULL,opening_cents INTEGER NOT NULL,closed_at TEXT,counted_cents INTEGER,expected_cents INTEGER);
CREATE TABLE IF NOT EXISTS saved_reports(id INTEGER PRIMARY KEY,created_at TEXT NOT NULL,start_on TEXT NOT NULL,end_on TEXT NOT NULL,snapshot_json TEXT NOT NULL);
'''


def now():
    return datetime.now().astimezone().isoformat(timespec='seconds')


def cents(value):
    try:
        value = float(value)
        result = round(value * 100)
    except (ValueError, TypeError, OverflowError):
        raise ValueError('Ingresa un importe válido.')
    if value < 0 or value > 100000000 or abs(value * 100 - result) > 0.00001:
        raise ValueError('El importe debe ser positivo y tener máximo dos decimales.')
    return result


def positive(value, label='cantidad'):
    try:
        x = float(value)
    except (ValueError, TypeError):
        raise ValueError(f'Ingresa una {label} válida.')
    if not 0 < x < 100000000 or x != x:
        raise ValueError(f'La {label} debe ser mayor que cero.')
    return x


def required(value, name):
    text = str(value or '').strip()
    if not text or len(text) > 160:
        raise ValueError(f'Ingresa {name} (máximo 160 caracteres).')
    return text


class Store:
    def __init__(self, path=DB_PATH):
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        with self.connect() as db:
            db.executescript(SCHEMA)
            db.executemany('INSERT OR IGNORE INTO products VALUES(?,?,?,?,?,?)',[(a,b,c,int(p*100),d,e) for a,b,c,p,d,e in MENU])
            db.executemany('INSERT OR IGNORE INTO inventory_items(name,unit,category) VALUES(?,?,?)',[
                ('Elote','pzas','Ingrediente'),('Crema','kg','Ingrediente'),('Mayonesa','kg','Ingrediente'),
                ('Queso','kg','Ingrediente'),('Chile','kg','Ingrediente'),('Limón','pzas','Ingrediente'),
                ('Tostitos','bolsas','Empaquetado'),('Maruchan','pzas','Empaquetado'),
                ('Vasos','pzas','Desechable'),('Cucharas','pzas','Desechable')])

    @contextmanager
    def connect(self):
        """Commit or roll back transactions and always close the SQLite handle."""
        db = sqlite3.connect(self.path, timeout=10)
        try:
            db.row_factory = sqlite3.Row
            db.execute('PRAGMA foreign_keys=ON')
            with db:
                yield db
        finally:
            db.close()

    def rows(self, query, params=()):
        with self.connect() as db:
            return [dict(row) for row in db.execute(query, params)]

    def bootstrap(self):
        return {'products':self.rows('SELECT * FROM products ORDER BY rowid'),
                'sales':self.sales(), 'inventory':self.inventory(), 'purchases':self.movements('purchases'),
                'expenses':self.movements('expenses'), 'cash':self.cash_status(), 'reports':self.reports()}

    def sales(self):
        return self.rows('SELECT * FROM sales ORDER BY id DESC LIMIT 100')

    def sale(self, items, payment='efectivo'):
        if payment not in ('efectivo','transferencia','otro'):
            raise ValueError('Selecciona una forma de pago válida.')
        if not isinstance(items, list) or not items or len(items)>80:
            raise ValueError('Agrega por lo menos un producto.')
        with self.connect() as db:
            chosen=[]
            for item in items:
                product=db.execute('SELECT * FROM products WHERE id=?',(item.get('id'),)).fetchone()
                if not product: raise ValueError('Producto inexistente.')
                quantity=item.get('quantity')
                if isinstance(quantity,bool) or not isinstance(quantity,int) or not 1<=quantity<=999:
                    raise ValueError('Cantidad no válida.')
                chosen.append((product,quantity))
            total=sum(p['price_cents']*q for p,q in chosen)
            cur=db.execute('INSERT INTO sales(created_at,payment,total_cents) VALUES(?,?,?)',(now(),payment,total))
            db.executemany('INSERT INTO sale_items(sale_id,product_id,product_name,description,quantity,unit_cents) VALUES(?,?,?,?,?,?)',[(cur.lastrowid,p['id'],p['name'],p['description'],q,p['price_cents']) for p,q in chosen])
            return {'id':cur.lastrowid,'total_cents':total}

    def inventory(self):
        return self.rows('''SELECT i.id,i.name,i.unit,i.category,
            ROUND(COALESCE((SELECT SUM(e.quantity) FROM stock_entries e WHERE e.item_id=i.id),0)
              +COALESCE((SELECT SUM(m.quantity) FROM stock_movements m JOIN stock_entries e ON e.id=m.entry_id WHERE e.item_id=i.id),0),3) quantity,
            (SELECT MIN(e.expires_on) FROM stock_entries e WHERE e.item_id=i.id AND e.expires_on IS NOT NULL AND e.quantity + COALESCE((SELECT SUM(m.quantity) FROM stock_movements m WHERE m.entry_id=e.id),0)>0) nearest_expiry
            FROM inventory_items i ORDER BY i.name''')

    def add_stock(self, item_id, quantity, expires_on='', notes=''):
        qty=positive(quantity)
        if expires_on:
            date.fromisoformat(expires_on)
        with self.connect() as db:
            if not db.execute('SELECT id FROM inventory_items WHERE id=?',(item_id,)).fetchone():
                raise ValueError('Insumo inexistente.')
            cur=db.execute('INSERT INTO stock_entries(item_id,quantity,created_at,expires_on,notes) VALUES(?,?,?,?,?)',(item_id,qty,now(),expires_on or None,str(notes or '')[:250]))
            return {'id':cur.lastrowid}

    def add_waste(self,item_id,quantity,reason):
        qty=positive(quantity)
        reason=required(reason,'el motivo de la merma')
        with self.connect() as db:
            entries=db.execute('''SELECT e.id,e.quantity+COALESCE(SUM(m.quantity),0) remaining
                FROM stock_entries e LEFT JOIN stock_movements m ON m.entry_id=e.id
                WHERE e.item_id=? GROUP BY e.id HAVING remaining>0
                ORDER BY (e.expires_on IS NULL),e.expires_on,e.created_at,e.id''',(item_id,)).fetchall()
            available=sum(x['remaining'] for x in entries)
            if available+1e-7<qty: raise ValueError('No hay suficientes existencias para registrar esa merma.')
            rest=qty
            for e in entries:
                if rest<=0.000001:break
                used=min(rest,e['remaining'])
                db.execute('INSERT INTO stock_movements(entry_id,quantity,kind,reason,created_at) VALUES(?,?,?,?,?)',(e['id'],-used,'merma',reason,now()))
                rest-=used
            return {'ok':True}

    def waste(self):
        return self.rows('''SELECT m.id,i.name,i.unit,-m.quantity quantity,m.reason,m.created_at
          FROM stock_movements m JOIN stock_entries e ON e.id=m.entry_id JOIN inventory_items i ON i.id=e.item_id
          WHERE m.kind='merma' ORDER BY m.id DESC LIMIT 100''')

    def movement(self,kind,concept,amount,payment='efectivo',notes=''):
        if kind not in ('purchases','expenses'):raise ValueError('Tipo de movimiento incorrecto.')
        concept=required(concept,'el concepto')
        if payment not in ('efectivo','transferencia','otro'):raise ValueError('Método de pago inválido.')
        with self.connect() as db:
            cur=db.execute(f'INSERT INTO {kind}(created_at,concept,amount_cents,payment,notes) VALUES(?,?,?,?,?)',(now(),concept,cents(amount),payment,str(notes or '')[:250]))
            return {'id':cur.lastrowid}

    def movements(self,kind):
        if kind not in ('purchases','expenses'):raise ValueError('Tipo incorrecto.')
        return self.rows(f'SELECT * FROM {kind} ORDER BY id DESC LIMIT 100')

    def cash_status(self):
        active=self.rows('SELECT * FROM cash_sessions WHERE closed_at IS NULL ORDER BY id DESC LIMIT 1')
        recent=self.rows('SELECT * FROM cash_sessions WHERE closed_at IS NOT NULL ORDER BY id DESC LIMIT 10')
        if not active:return {'active':None,'recent':recent}
        a=active[0]
        return {'active':{**a,'expected_cents':self.expected_cash(a['opened_at'])+a['opening_cents']},'recent':recent}

    def expected_cash(self,opened):
        with self.connect() as db:
            sales=db.execute("SELECT COALESCE(SUM(total_cents),0) FROM sales WHERE payment='efectivo' AND created_at>=?",(opened,)).fetchone()[0]
            buys=db.execute("SELECT COALESCE(SUM(amount_cents),0) FROM purchases WHERE payment='efectivo' AND created_at>=?",(opened,)).fetchone()[0]
            exp=db.execute("SELECT COALESCE(SUM(amount_cents),0) FROM expenses WHERE payment='efectivo' AND created_at>=?",(opened,)).fetchone()[0]
            return sales-buys-exp

    def cash_open(self,amount):
        with self.connect() as db:
            if db.execute('SELECT 1 FROM cash_sessions WHERE closed_at IS NULL').fetchone():raise ValueError('Ya existe una jornada abierta.')
            db.execute('INSERT INTO cash_sessions(opened_at,opening_cents) VALUES(?,?)',(now(),cents(amount)))
        return self.cash_status()

    def cash_close(self,counted):
        with self.connect() as db:
            a=db.execute('SELECT * FROM cash_sessions WHERE closed_at IS NULL ORDER BY id DESC LIMIT 1').fetchone()
            if not a:raise ValueError('No hay una jornada abierta.')
            expected=a['opening_cents']+self.expected_cash(a['opened_at'])
            db.execute('UPDATE cash_sessions SET closed_at=?,counted_cents=?,expected_cents=? WHERE id=?',(now(),cents(counted),expected,a['id']))
        return self.cash_status()

    def reports(self):
        return self.rows('SELECT id,created_at,start_on,end_on FROM saved_reports ORDER BY id DESC')

    def report(self,report_id):
        result=self.rows('SELECT * FROM saved_reports WHERE id=?',(report_id,))
        if not result:raise ValueError('Reporte no encontrado.')
        item=result[0]
        item['snapshot']=json.loads(item.pop('snapshot_json'))
        return item

    def generate_report(self, start_on):
        start=date.fromisoformat(start_on)
        if start.weekday()!=0:raise ValueError('Selecciona un lunes como inicio de semana.')
        end=start+timedelta(days=6)
        params=(start.isoformat(),end.isoformat())
        def within(column):return f'substr({column},1,10) BETWEEN ? AND ?'
        data={
            'sales_by_day':self.rows(f'SELECT substr(created_at,1,10) day,COUNT(*) orders,SUM(total_cents) total_cents FROM sales WHERE {within("created_at")} GROUP BY day ORDER BY day',params),
            'products':self.rows(f'''SELECT si.product_name name,si.description,SUM(si.quantity) units,SUM(si.quantity*si.unit_cents) total_cents
                FROM sale_items si JOIN sales s ON s.id=si.sale_id WHERE {within('s.created_at')}
                GROUP BY si.product_id ORDER BY units DESC''',params),
            'purchases':self.rows(f'SELECT created_at,concept,amount_cents,payment FROM purchases WHERE {within("created_at")} ORDER BY id',params),
            'expenses':self.rows(f'SELECT created_at,concept,amount_cents,payment FROM expenses WHERE {within("created_at")} ORDER BY id',params),
            'waste':self.rows(f'''SELECT i.name,ROUND(SUM(-m.quantity),3) quantity,i.unit FROM stock_movements m JOIN stock_entries e ON e.id=m.entry_id JOIN inventory_items i ON i.id=e.item_id WHERE {within('m.created_at')} AND m.kind='merma' GROUP BY i.id''',params)
        }
        data['sales_total_cents']=sum(x['total_cents'] for x in data['sales_by_day'])
        data['purchases_total_cents']=sum(x['amount_cents'] for x in data['purchases'])
        data['expenses_total_cents']=sum(x['amount_cents'] for x in data['expenses'])
        with self.connect() as db:
            cur=db.execute('INSERT INTO saved_reports(created_at,start_on,end_on,snapshot_json) VALUES(?,?,?,?)',(now(),start.isoformat(),end.isoformat(),json.dumps(data,ensure_ascii=False)))
        return self.report(cur.lastrowid)


class Api:
    """Puente expuesto a JavaScript por pywebview."""
    def __init__(self,store=None):self.store=store or Store()
    def call(self,action,payload=None):
        payload=payload or {}
        actions={
            'bootstrap':lambda:self.store.bootstrap(),
            'sale':lambda:self.store.sale(payload['items'],payload.get('payment','efectivo')),
            'add_stock':lambda:self.store.add_stock(payload['item_id'],payload['quantity'],payload.get('expires_on',''),payload.get('notes','')),
            'add_waste':lambda:self.store.add_waste(payload['item_id'],payload['quantity'],payload['reason']),
            'waste':self.store.waste,
            'movement':lambda:self.store.movement(payload['kind'],payload['concept'],payload['amount'],payload.get('payment','efectivo'),payload.get('notes','')),
            'cash_open':lambda:self.store.cash_open(payload['amount']),
            'cash_close':lambda:self.store.cash_close(payload['amount']),
            'report_generate':lambda:self.store.generate_report(payload['start_on']),
            'report_get':lambda:self.store.report(payload['id']),
        }
        try:
            if action not in actions:raise ValueError('Operación desconocida.')
            return {'ok':True,'data':actions[action]()}
        except (ValueError,KeyError,sqlite3.Error) as exc:
            return {'ok':False,'error':str(exc)}


def run():
    if not FRONTEND_PATH.is_file():
        raise FileNotFoundError(f'No se encontró la interfaz: {FRONTEND_PATH}. Verifica que la carpeta _internal/frontend se haya incluido en el paquete.')
    import webview  # Solo se requiere al abrir la aplicación de escritorio.
    api = Api()  # Crea la base de datos en DATA_ROOT/data cuando todavía no existe.
    webview.create_window('Maíz Urbano — Gestión local', str(FRONTEND_PATH), js_api=api,
                          width=1360, height=850, min_size=(1024, 640), background_color='#FFF9EF')
    webview.start(debug=False)


def self_check():
    """Smoke test for packaged Windows binary without opening a GUI.

    Confirms bundled UI assets and writable SQLite next to the executable.
    Temporary test records are deleted after the check.
    """
    for relative in ('index.html', 'styles.css', 'app.js'):
        asset = RESOURCE_ROOT / 'frontend' / relative
        if not asset.is_file():
            raise FileNotFoundError(f'Recurso no incluido en el ejecutable: {asset}')
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='maiz-smoke-', dir=DB_PATH.parent) as temp:
        db = Path(temp) / 'probe.db'
        store = Store(db)
        store.sale([{'id': 'tostielote', 'quantity': 1}])
        if Store(db).sales()[0]['total_cents'] != 7000:
            raise RuntimeError('Error de persistencia SQLite en la distribución.')
    return True


if __name__ == '__main__':
    if len(sys.argv) == 2 and sys.argv[1] == '--self-check':
        self_check()
    else:
        run()