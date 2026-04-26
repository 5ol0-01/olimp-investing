import random
import json
import os
import urllib.request
import threading
from datetime import datetime, timedelta
from kivy.clock import Clock
from kivy.graphics import Color, Line, Rectangle, Ellipse, RoundedRectangle
from kivymd.app import MDApp
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDRaisedButton, MDFillRoundFlatButton, MDFlatButton, MDIconButton
from kivymd.uix.card import MDCard
from kivymd.uix.toolbar import MDTopAppBar
from kivymd.uix.bottomnavigation import MDBottomNavigation, MDBottomNavigationItem
from kivymd.uix.dialog import MDDialog
from kivymd.uix.textfield import MDTextField
from kivymd.uix.list import MDList
from kivymd.uix.progressbar import MDProgressBar
from kivymd.uix.screen import MDScreen
from kivy.uix.widget import Widget
from kivy.uix.scrollview import ScrollView
from kivy.uix.floatlayout import FloatLayout
from kivy.metrics import dp
from kivy.animation import Animation
from kivy.utils import get_color_from_hex


# ==================== ЦВЕТОВАЯ СХЕМА (СВЕТЛАЯ) ====================

COLORS = {
    'bg': '#F0F2F5',
    'bg_card': '#FFFFFF',
    'bg_card_hover': '#F8F9FA',
    'accent': '#1565C0',
    'accent_light': '#1E88E5',
    'green': '#2E7D32',
    'green_light': '#E8F5E9',
    'red': '#C62828',
    'red_light': '#FFEBEE',
    'gold': '#F9A825',
    'text': '#212121',
    'text_secondary': '#616161',
    'divider': '#E0E0E0',
    'border': '#E8E8E8',
}

# ==================== ДАННЫЕ ====================

REAL_HISTORY_BACKUP = {
    "SBER": [265.0, 267.2, 268.5, 270.1, 269.8, 271.3, 272.0, 273.5, 274.2, 275.8,
             276.3, 277.1, 278.0, 279.4, 280.2, 281.5, 282.0, 283.3, 284.1, 284.8,
             285.2, 286.0, 285.8, 286.5, 287.0, 287.8, 288.2, 289.0, 288.7, 289.5],
    "YDEX": [3800.0, 3820.5, 3850.0, 3870.2, 3890.8, 3910.3, 3930.1, 3950.6, 3970.4, 3990.0,
             4010.2, 4030.5, 4050.8, 4070.3, 4090.1, 4110.6, 4130.2, 4150.0, 4170.5, 4190.8,
             4160.3, 4140.1, 4120.6, 4100.2, 4080.5, 4060.8, 4040.3, 4020.1, 4000.6, 4150.0],
    "GAZP": [120.0, 120.5, 121.0, 121.5, 122.0, 122.5, 123.0, 123.5, 124.0, 124.5,
             125.0, 125.5, 126.0, 126.5, 127.0, 127.5, 128.0, 127.5, 127.0, 126.5,
             126.0, 125.5, 125.0, 124.5, 124.0, 123.5, 123.0, 122.5, 122.0, 126.0],
    "LKOH": [7000.0, 7020.0, 7040.0, 7060.0, 7080.0, 7100.0, 7120.0, 7140.0, 7160.0, 7180.0,
             7200.0, 7220.0, 7240.0, 7260.0, 7280.0, 7300.0, 7320.0, 7340.0, 7360.0, 7380.0,
             7400.0, 7380.0, 7360.0, 7340.0, 7320.0, 7300.0, 7280.0, 7260.0, 7240.0, 7420.0],
    "ROSN": [450.0, 452.0, 454.0, 456.0, 458.0, 460.0, 462.0, 464.0, 466.0, 468.0,
             470.0, 472.0, 474.0, 476.0, 478.0, 480.0, 482.0, 484.0, 482.0, 480.0,
             478.0, 476.0, 474.0, 472.0, 470.0, 468.0, 466.0, 464.0, 462.0, 482.0],
    "TATN": [560.0, 562.0, 564.0, 566.0, 568.0, 570.0, 572.0, 574.0, 576.0, 578.0,
             580.0, 582.0, 584.0, 586.0, 588.0, 590.0, 592.0, 590.0, 588.0, 586.0,
             584.0, 582.0, 580.0, 578.0, 576.0, 574.0, 572.0, 570.0, 568.0, 590.0],
    "NVTK": [1200.0, 1210.0, 1220.0, 1230.0, 1240.0, 1250.0, 1260.0, 1270.0, 1280.0, 1290.0,
             1300.0, 1310.0, 1320.0, 1330.0, 1340.0, 1350.0, 1360.0, 1370.0, 1380.0, 1390.0,
             1400.0, 1410.0, 1420.0, 1430.0, 1440.0, 1450.0, 1440.0, 1430.0, 1420.0, 1450.0],
    "GMKN": [15000.0, 15100.0, 15200.0, 15300.0, 15400.0, 15500.0, 15600.0, 15700.0, 15800.0, 15900.0,
             16000.0, 15900.0, 15800.0, 15700.0, 15600.0, 15500.0, 15400.0, 15300.0, 15200.0, 15100.0,
             15200.0, 15300.0, 15400.0, 15500.0, 15600.0, 15700.0, 15800.0, 15700.0, 15600.0, 15800.0],
    "VTBR": [0.018, 0.019, 0.020, 0.021, 0.022, 0.023, 0.024, 0.025, 0.026, 0.027,
             0.028, 0.029, 0.030, 0.031, 0.032, 0.033, 0.034, 0.035, 0.036, 0.037,
             0.038, 0.039, 0.040, 0.041, 0.042, 0.043, 0.044, 0.045, 0.046, 0.045],
}

BLUE_CHIPS = ["SBER", "YDEX", "GAZP", "LKOH", "ROSN", "TATN", "NVTK", "GMKN", "VTBR"]

SECTORS = {
    "Нефть": ["LKOH", "ROSN", "TATN", "SNGS", "NVTK", "TRNFP", "SIBN"],
    "Банки": ["SBER", "VTBR", "TCSG"],
    "IT": ["YDEX", "AFKS", "RTKM"],
    "Металлы": ["GMKN", "PLZL", "RUAL", "CHMF", "NLMK", "MAGN"],
    "Ритейл": ["FIXP", "MGNT", "DSKY"],
    "Энергетика": ["HYDR", "FEES", "UPRO", "IRAO", "OGKB"],
    "Транспорт": ["AFLT", "NMTP", "UNAC"],
    "Химия": ["PHOR", "AKRN"],
    "Строительство": ["PIKK", "LSRG", "ETAL"],
}

POPULAR_TICKERS = {"SBER": 1, "GAZP": 2, "LKOH": 3, "YDEX": 4, "ROSN": 5, "TATN": 6,
                   "NVTK": 7, "GMKN": 8, "VTBR": 9, "TRNFP": 10, "PLZL": 11, "CHMF": 12,
                   "MAGN": 13, "PHOR": 14, "TGKB": 15, "RTKM": 16, "AFLT": 17, "MGNT": 18}

CACHE_FILE = 'moex_cache.json'


def load_cache():
    if os.path.exists(CACHE_FILE):
        try:
            with open(CACHE_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            pass
    return {}


def save_cache(cache_data):
    try:
        with open(CACHE_FILE, 'w', encoding='utf-8') as f:
            json.dump(cache_data, f, ensure_ascii=False, indent=2)
    except:
        pass


def get_moex_price(ticker):
    url = f"https://iss.moex.com/iss/engines/stock/markets/shares/securities/{ticker}.json"
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=5) as response:
            data = json.loads(response.read().decode('utf-8'))
        marketdata = data.get('marketdata', {}).get('data', [])
        if marketdata and marketdata[0][12]:
            return float(marketdata[0][12])
        securities = data.get('securities', {}).get('data', [])
        if securities and securities[0][13]:
            return float(securities[0][13])
    except:
        pass
    return None


def get_moex_all_stocks():
    url = "https://iss.moex.com/iss/engines/stock/markets/shares/securities.json"
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=10) as response:
            data = json.loads(response.read().decode('utf-8'))
        securities = data.get('securities', {}).get('data', [])
        stocks = []
        for sec in securities:
            ticker = sec[0]
            name = sec[2] if len(sec) > 2 else ticker
            price = sec[13] if len(sec) > 13 and sec[13] else 0
            lot = sec[15] if len(sec) > 15 and sec[15] else 1
            sector = "Прочее"
            for s_name, s_tickers in SECTORS.items():
                if ticker in s_tickers:
                    sector = s_name
                    break
            stocks.append({
                'ticker': ticker, 'name': name,
                'price': float(price) if price else 0,
                'sector': sector, 'lot': int(lot) if lot else 1,
            })
        return stocks
    except:
        return None


STOCKS_INFO = {
    "SBER": {"name": "Сбербанк", "price": 284.0, "sector": "Банки", "lot": 10,
             "description": "Крупнейший банк России.", "country": "Россия",
             "capitalization": "5.2 трлн ₽", "type": "Акции", "ticker": "SBER",
             "dividends": {"current": {"date_close": "2026-07-15", "date_pay": "2026-07-30", "amount": 12.5},
                           "history": [{"year": 2025, "amount": 10.2, "date_pay": "2025-07-20"}]}},
    "YDEX": {"name": "Яндекс", "price": 4150.0, "sector": "IT", "lot": 1,
             "description": "Ведущая IT-компания.", "country": "Нидерланды",
             "capitalization": "1.3 трлн ₽", "type": "Акции", "ticker": "YDEX",
             "dividends": {"current": None, "history": []}},
    "GAZP": {"name": "Газпром", "price": 126.0, "sector": "Энергетика", "lot": 10,
             "description": "Глобальная энергетическая компания.", "country": "Россия",
             "capitalization": "3.0 трлн ₽", "type": "Акции", "ticker": "GAZP",
             "dividends": {"current": {"date_close": "2026-09-20", "date_pay": "2026-10-05", "amount": 8.2}, "history": []}},
    "LKOH": {"name": "ЛУКОЙЛ", "price": 7420.0, "sector": "Нефть", "lot": 1,
             "description": "Крупнейшая нефтяная компания.", "country": "Россия",
             "capitalization": "4.8 трлн ₽", "type": "Акции", "ticker": "LKOH",
             "dividends": {"current": {"date_close": "2026-08-05", "date_pay": "2026-08-20", "amount": 25.0}, "history": []}},
    "ROSN": {"name": "Роснефть", "price": 482.0, "sector": "Нефть", "lot": 1,
             "description": "Лидер нефтяной отрасли.", "country": "Россия",
             "capitalization": "5.1 трлн ₽", "type": "Акции", "ticker": "ROSN",
             "dividends": {"current": {"date_close": "2026-07-01", "date_pay": "2026-07-15", "amount": 18.3}, "history": []}},
    "TATN": {"name": "Татнефть", "price": 590.0, "sector": "Нефть", "lot": 1,
             "description": "Крупная нефтяная компания.", "country": "Россия",
             "capitalization": "1.2 трлн ₽", "type": "Акции", "ticker": "TATN",
             "dividends": {"current": {"date_close": "2026-06-28", "date_pay": "2026-07-12", "amount": 8.2}, "history": []}},
    "NVTK": {"name": "НОВАТЭК", "price": 1450.0, "sector": "Нефть", "lot": 1,
             "description": "Крупнейший независимый производитель газа.", "country": "Россия",
             "capitalization": "4.3 трлн ₽", "type": "Акции", "ticker": "NVTK",
             "dividends": {"current": None, "history": []}},
    "GMKN": {"name": "Норникель", "price": 15800.0, "sector": "Металлы", "lot": 1,
             "description": "Крупнейший производитель никеля и палладия.", "country": "Россия",
             "capitalization": "2.5 трлн ₽", "type": "Акции", "ticker": "GMKN",
             "dividends": {"current": {"date_close": "2026-10-01", "date_pay": "2026-10-15", "amount": 450.0}, "history": []}},
    "VTBR": {"name": "ВТБ", "price": 0.045, "sector": "Банки", "lot": 10000,
             "description": "ВТБ — второй по величине банк России.", "country": "Россия",
             "capitalization": "1.8 трлн ₽", "type": "Акции", "ticker": "VTBR",
             "dividends": {"current": None, "history": []}},
}


# ==================== ГРАФИК ====================

class StockChart(FloatLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.history_data = []
        self.period = "LIVE"
        self.base_price = 0
        self.labels_layout = FloatLayout()
        self.add_widget(self.labels_layout)
        self.drawing_widget = Widget()
        self.add_widget(self.drawing_widget)
        self._need_update_labels = True
        self.bind(size=lambda *x: setattr(self, '_need_update_labels', True))
        self.bind(pos=lambda *x: setattr(self, '_need_update_labels', True))
        Clock.schedule_interval(self.draw_graph, 0.5)
    
    def set_history(self, history_data):
        if history_data and len(history_data) > 5:
            self.history_data = history_data[:]
            self.base_price = self.history_data[-1]
    
    def set_period(self, period):
        self.period = period
        self._need_update_labels = True
    
    def _get_prices_for_period(self):
        if not self.history_data:
            return [self.base_price] * 10
        if self.period == "LIVE":
            return self.history_data[-40:] if len(self.history_data) >= 40 else self.history_data
        elif self.period == "7D":
            return self.history_data[-7:] if len(self.history_data) >= 7 else self.history_data
        elif self.period == "30D":
            return self.history_data[-30:] if len(self.history_data) >= 30 else self.history_data
        elif self.period in ("1Y", "ALL"):
            return self.history_data[-252:] if len(self.history_data) >= 252 else self.history_data
        return self.history_data
    
    def get_period_change(self):
        prices = self._get_prices_for_period()
        if len(prices) < 2:
            return 0, 0, 0
        return prices[-1], prices[-1] - prices[0], ((prices[-1] - prices[0]) / prices[0] * 100) if prices[0] != 0 else 0
    
    def _update_labels(self):
        if self.labels_layout in self.children:
            self.remove_widget(self.labels_layout)
        self.labels_layout = FloatLayout()
        self.add_widget(self.labels_layout)
        prices = self._get_prices_for_period()
        if len(prices) < 2:
            return
        ml, mr, mt, mb = dp(55), dp(10), dp(15), dp(25)
        pw, ph = self.width - ml - mr, self.height - mt - mb
        mn, mx = min(prices), max(prices)
        rng = mx - mn if mx != mn else 1.0
        for i in range(4):
            yp = self.y + mb + (ph * i / 3)
            self.labels_layout.add_widget(MDLabel(
                text=f"{mx - (rng * i / 3):.1f}", font_style="Caption",
                size_hint=(None, None), size=(dp(50), dp(16)),
                pos=(self.x + dp(3), yp - dp(8)), halign="right",
                theme_text_color="Custom", text_color=[0.4, 0.4, 0.4, 1], font_size=dp(11)))
        nv = min(5, len(prices))
        for i in range(nv + 1):
            xp = self.x + ml + (pw * i / nv) if nv > 0 else self.x + ml
            idx = int(i * (len(prices) - 1) / nv) if nv > 0 else 0
            if idx < len(prices):
                if self.period == "7D":
                    dt = f"-{len(prices) - idx - 1}д"
                elif self.period == "30D":
                    dt = f"-{len(prices) - idx - 1}д"
                elif self.period in ("1Y", "ALL"):
                    dt = f"-{int((len(prices) - idx - 1) / 21) + 1}м"
                else:
                    dt = f"{idx+1}"
                self.labels_layout.add_widget(MDLabel(
                    text=dt, font_style="Caption", size_hint=(None, None),
                    size=(dp(40), dp(14)), pos=(xp - dp(20), self.y + dp(8)),
                    halign="center", theme_text_color="Custom",
                    text_color=[0.5, 0.5, 0.5, 1], font_size=dp(10)))
        self._need_update_labels = False
    
    def draw_graph(self, *args):
        self.drawing_widget.canvas.clear()
        if self._need_update_labels:
            self._update_labels()
        prices = self._get_prices_for_period()
        if len(prices) < 2:
            return
        ml, mr, mt, mb = dp(55), dp(10), dp(15), dp(25)
        pw, ph = self.width - ml - mr, self.height - mt - mb
        mn, mx = min(prices), max(prices)
        rng = mx - mn if mx != mn else 1.0
        xs = pw / (len(prices) - 1) if len(prices) > 1 else 1
        with self.drawing_widget.canvas:
            Color(*get_color_from_hex('#FAFAFA'))
            Rectangle(pos=(self.x + ml, self.y + mb), size=(pw, ph))
            for i in range(4):
                yp = self.y + mb + (ph * i / 3)
                Color(*get_color_from_hex('#E0E0E0'))
                Line(points=[self.x + ml, yp, self.x + ml + pw, yp], width=dp(0.5))
            nv = min(5, len(prices))
            Color(*get_color_from_hex('#E0E0E0'))
            for i in range(nv + 1):
                xp = self.x + ml + (pw * i / nv) if nv > 0 else self.x + ml
                Line(points=[xp, self.y + mb, xp, self.y + mb + ph], width=dp(0.3))
            Color(*get_color_from_hex('#1565C0'))
            pts = []
            for i, p in enumerate(prices):
                pts.extend([self.x + ml + i * xs, self.y + mb + ((p - mn) / rng) * ph])
            Line(points=pts, width=dp(2), joint='round')


class VerticalDivider(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.size_hint_x = None
        self.width = dp(1)
        self.bind(size=self._draw, pos=self._draw)
        Clock.schedule_once(self._draw, 0.05)
    def _draw(self, *args):
        self.canvas.clear()
        if self.height > 0:
            with self.canvas:
                Color(*get_color_from_hex('#E0E0E0'))
                Line(points=[self.x + 1, self.y + dp(8), self.x + 1, self.y + self.height - dp(8)], width=dp(1))


# ==================== ДИАЛОГ АКЦИИ ====================

class StockDetailDialog:
    def __init__(self, app, symbol):
        self.app = app
        self.symbol = symbol
        self.stock = STOCKS_INFO.get(symbol, {"name": symbol, "price": 0, "sector": "Прочее"})
        self.chart = None
        self.period_buttons = {}
        self.period_change_label = None
        self.dialog = None
        self.detail_content = None
    
    def show(self):
        content = MDBoxLayout(orientation='vertical', spacing=dp(5), size_hint_y=None, height=dp(580))
        self.chart = StockChart()
        history = self.app.get_stock_history(self.symbol)
        if history:
            self.chart.set_history(history)
        period_row = MDBoxLayout(orientation='horizontal', size_hint_y=None, height=dp(30), spacing=dp(3), padding=[dp(5), 0])
        for pid, pname in [("LIVE", "Live"), ("7D", "7д"), ("30D", "30д"), ("1Y", "1г"), ("ALL", "Всё")]:
            btn = MDFlatButton(text=pname, font_style="Caption", size_hint_x=None, width=dp(42))
            btn.bind(on_release=lambda x, p=pid: self.set_chart_period(p))
            period_row.add_widget(btn)
            self.period_buttons[pid] = btn
        content.add_widget(period_row)
        self.period_change_label = MDLabel(text="", font_style="Caption", halign="right", size_hint_y=None, height=dp(18), theme_text_color="Custom")
        content.add_widget(self.period_change_label)
        chart_card = MDCard(radius=[15], md_bg_color=get_color_from_hex('#FFFFFF'), size_hint_y=None, height=dp(200))
        chart_card.add_widget(self.chart)
        content.add_widget(chart_card)
        data = self.app.portfolio.get(self.symbol, [0, 0.0])
        count = data[0] if isinstance(data, list) else 0
        cost = data[1] if isinstance(data, list) and len(data) > 1 else 0.0
        avg_price = cost / count if count > 0 else 0
        cp = self.stock.get('price', 0)
        cv = count * cp
        profit = cv - cost
        pp = (profit / cost * 100) if cost > 0 else 0
        content.add_widget(MDLabel(
            text=f"Ср: {avg_price:.0f}₽ | Тек: {cp:.4f}₽ | {count} шт | {cv:,.0f}₽\nИзм: {profit:+,.0f}₽ ({pp:+.1f}%)",
            halign="left", size_hint_y=None, height=dp(40), theme_text_color="Custom", text_color=get_color_from_hex('#212121')))
        btn_row = MDBoxLayout(orientation='horizontal', size_hint_y=None, height=dp(45), spacing=dp(10), padding=[dp(20), 0])
        buy_btn = MDRaisedButton(text="КУПИТЬ", md_bg_color=get_color_from_hex('#2E7D32'), size_hint_x=0.5)
        buy_btn.bind(on_release=lambda x: self.app.open_trade_dialog(self.symbol, "BUY"))
        btn_row.add_widget(buy_btn)
        sell_btn = MDRaisedButton(text="ПРОДАТЬ", md_bg_color=get_color_from_hex('#C62828'), size_hint_x=0.5)
        sell_btn.bind(on_release=lambda x: self.app.open_trade_dialog(self.symbol, "SELL"))
        btn_row.add_widget(sell_btn)
        content.add_widget(btn_row)
        tab_btns = MDBoxLayout(orientation='horizontal', size_hint_y=None, height=dp(35), spacing=dp(5), padding=[dp(10), 0])
        self.overview_btn = MDFlatButton(text="Обзор")
        self.overview_btn.bind(on_release=lambda x: self.switch_tab("overview"))
        self.div_btn = MDFlatButton(text="Дивиденды")
        self.div_btn.bind(on_release=lambda x: self.switch_tab("dividends"))
        tab_btns.add_widget(self.overview_btn)
        tab_btns.add_widget(self.div_btn)
        content.add_widget(tab_btns)
        self.detail_content = ScrollView(size_hint_y=1)
        content.add_widget(self.detail_content)
        self.dialog = MDDialog(title=f"{self.stock.get('name', self.symbol)} ({self.symbol})", type="custom", content_cls=content,
                               buttons=[MDFlatButton(text="ЗАКРЫТЬ", on_release=lambda x: self.dialog.dismiss())])
        self.set_chart_period("LIVE")
        self.switch_tab("overview")
        self.dialog.open()
    
    def switch_tab(self, tab_name):
        self.detail_content.clear_widgets()
        if tab_name == "overview":
            self.overview_btn.text_color = get_color_from_hex('#1565C0')
            self.div_btn.text_color = [0.5, 0.5, 0.5, 1]
            info = self.stock
            box = MDBoxLayout(orientation='vertical', size_hint_y=None, spacing=dp(2), padding=[dp(5), dp(5)])
            box.bind(minimum_height=box.setter('height'))
            fields = [
                ("Описание", info.get('description', '-')), ("Страна", info.get('country', '-')),
                ("Капитализация", info.get('capitalization', '-')), ("Тип", info.get('type', 'Акции')),
                ("Тикер", info.get('ticker', self.symbol)), ("Сектор", info.get('sector', 'Прочее')),
                ("Биржа", "MOEX"), ("Лот", str(info.get('lot', 1))),
                ("Квал.", info.get('qualified', 'Нет'))
            ]
            for fn, fv in fields:
                row = MDBoxLayout(orientation='horizontal', size_hint_y=None, height=dp(32), padding=[dp(10), dp(5)])
                row.add_widget(MDLabel(text=fn, size_hint_x=0.45, font_style="Caption", theme_text_color="Secondary"))
                row.add_widget(MDLabel(text=fv, size_hint_x=0.55, font_style="Caption", theme_text_color="Custom", text_color=get_color_from_hex('#212121')))
                box.add_widget(row)
            self.detail_content.add_widget(box)
        else:
            self.overview_btn.text_color = [0.5, 0.5, 0.5, 1]
            self.div_btn.text_color = get_color_from_hex('#1565C0')
            self._build_dividends()
    
    def _build_dividends(self):
        box = MDBoxLayout(orientation='vertical', size_hint_y=None, spacing=dp(10), padding=[dp(10), dp(10)])
        box.bind(minimum_height=box.setter('height'))
        div_data = self.stock.get('dividends', {})
        if isinstance(div_data, dict):
            current_div = div_data.get('current')
            if current_div:
                card = MDCard(size_hint_y=None, height=dp(140), padding=dp(12), md_bg_color=get_color_from_hex('#E8F5E9'), radius=[10])
                cb = MDBoxLayout(orientation='vertical', spacing=dp(5))
                try: days_left = (datetime.strptime(current_div['date_close'], "%Y-%m-%d") - datetime.now()).days
                except: days_left = 999
                amount = current_div['amount']
                div_yield = (amount / self.stock.get('price', 1)) * 100
                cb.add_widget(MDLabel(text="Ближайшие дивиденды", bold=True, font_style="Subtitle1", theme_text_color="Custom", text_color=get_color_from_hex('#2E7D32')))
                cb.add_widget(MDLabel(text=f"Реестр: {current_div['date_close']} ({days_left} дн)", font_style="Caption"))
                cb.add_widget(MDLabel(text=f"{amount:.1f} ₽/акц ({div_yield:.2f}%)", font_style="Caption"))
                cb.add_widget(MDLabel(text=f"Выплата: {current_div['date_pay']}", font_style="Caption"))
                data = self.app.portfolio.get(self.symbol, [0, 0.0])
                cnt = data[0] if isinstance(data, list) else 0
                if cnt > 0:
                    cb.add_widget(MDLabel(text=f"У вас: {cnt} акций = {cnt * amount:,.0f} ₽", font_style="Caption",
                                          theme_text_color="Custom", text_color=get_color_from_hex('#2E7D32')))
                card.add_widget(cb)
                box.add_widget(card)
            else:
                box.add_widget(MDLabel(text="Нет предстоящих дивидендов", font_style="Caption", theme_text_color="Secondary"))
            box.add_widget(MDLabel(text="История выплат", bold=True, font_style="Subtitle1", size_hint_y=None, height=dp(30), theme_text_color="Custom", text_color=get_color_from_hex('#212121')))
            for h in div_data.get('history', []):
                yld = (h['amount'] / self.stock.get('price', 1)) * 100 if self.stock.get('price', 0) > 0 else 0
                row = MDBoxLayout(orientation='horizontal', size_hint_y=None, height=dp(28), padding=[dp(10), dp(3)])
                row.add_widget(MDLabel(text=str(h['year']), size_hint_x=0.2, font_style="Caption"))
                row.add_widget(MDLabel(text=f"{h['amount']:.1f} ₽", size_hint_x=0.4, font_style="Caption", halign="center"))
                row.add_widget(MDLabel(text=f"{yld:.2f}%", size_hint_x=0.2, font_style="Caption", halign="center"))
                row.add_widget(MDLabel(text=h['date_pay'], size_hint_x=0.2, font_style="Caption", halign="right"))
                box.add_widget(row)
        else:
            box.add_widget(MDLabel(text="Нет данных о дивидендах", font_style="Caption", theme_text_color="Secondary"))
        self.detail_content.add_widget(box)
    
    def set_chart_period(self, period):
        self.chart.set_period(period)
        for pid, btn in self.period_buttons.items():
            btn.md_bg_color = get_color_from_hex('#1565C0') if pid == period else get_color_from_hex('#E0E0E0')
            btn.text_color = get_color_from_hex('#FFFFFF') if pid == period else get_color_from_hex('#616161')
        lp, ch, pct = self.chart.get_period_change()
        color = get_color_from_hex('#2E7D32') if ch >= 0 else get_color_from_hex('#C62828')
        self.period_change_label.text = f"{'▲' if ch >= 0 else '▼'} {ch:+.2f} ₽ ({pct:+.2f}%)"
        self.period_change_label.text_color = color


# ==================== ДИАЛОГ МОИ ДИВИДЕНДЫ ====================

class MyDividendsDialog:
    def __init__(self, app):
        self.app = app
    def show(self):
        content = MDBoxLayout(orientation='vertical', spacing=dp(10), size_hint_y=None, height=dp(500))
        scroll = ScrollView()
        box = MDBoxLayout(orientation='vertical', size_hint_y=None, spacing=dp(10), padding=[dp(10), dp(10)])
        box.bind(minimum_height=box.setter('height'))
        total = 0
        for symbol, info in STOCKS_INFO.items():
            data = self.app.portfolio.get(symbol, [0, 0.0])
            cnt = data[0] if isinstance(data, list) else 0
            if cnt <= 0: continue
            div_data = info.get('dividends', {})
            if isinstance(div_data, dict):
                current = div_data.get('current')
                card = MDCard(size_hint_y=None, height=dp(120) if current else dp(60), padding=dp(12),
                              md_bg_color=get_color_from_hex('#FFFFFF'), radius=[10])
                cb = MDBoxLayout(orientation='vertical', spacing=dp(3))
                cb.add_widget(MDLabel(text=f"{symbol} — {info['name']}", bold=True, font_style="Subtitle1", theme_text_color="Custom", text_color=get_color_from_hex('#212121')))
                cb.add_widget(MDLabel(text=f"{cnt} акций", font_style="Caption", theme_text_color="Secondary"))
                if current:
                    try: days_left = (datetime.strptime(current['date_close'], "%Y-%m-%d") - datetime.now()).days
                    except: days_left = 999
                    amount = current['amount']
                    expected = cnt * amount
                    total += expected
                    cb.add_widget(MDLabel(text=f"{current['date_close']} ({days_left} дн) | {amount:.1f} ₽", font_style="Caption"))
                    cb.add_widget(MDLabel(text=f"{expected:,.0f} ₽ | После налога: {expected * 0.87:,.0f} ₽", font_style="Caption",
                                          theme_text_color="Custom", text_color=get_color_from_hex('#2E7D32')))
                else:
                    cb.add_widget(MDLabel(text="Нет данных о дивидендах", font_style="Caption", theme_text_color="Secondary"))
                card.add_widget(cb)
                box.add_widget(card)
        if total > 0:
            box.add_widget(MDLabel(text=f"Всего: {total:,.0f} ₽ | После налога: {total * 0.87:,.0f} ₽",
                                   font_style="Subtitle1", halign="center", size_hint_y=None, height=dp(40),
                                   theme_text_color="Custom", text_color=get_color_from_hex('#2E7D32')))
        scroll.add_widget(box)
        content.add_widget(scroll)
        dialog = MDDialog(title="Мои дивиденды", type="custom", content_cls=content,
                          buttons=[MDFlatButton(text="ЗАКРЫТЬ", on_release=lambda x: dialog.dismiss())])
        dialog.open()


# ==================== ЭКРАН ЗАГРУЗКИ ====================

class LoadingScreen(MDScreen):
    def __init__(self, app, **kwargs):
        super().__init__(**kwargs)
        self.app = app
        self.md_bg_color = get_color_from_hex('#F0F2F5')
        layout = MDBoxLayout(orientation='vertical', padding=dp(40), spacing=dp(20))
        layout.add_widget(Widget(size_hint_y=0.3))
        layout.add_widget(MDLabel(text="Olimp Investing", font_style="H3", halign="center", size_hint_y=None, height=dp(60),
                                  theme_text_color="Custom", text_color=get_color_from_hex('#1565C0')))
        self.message_label = MDLabel(text="Загружаем актуальные данные с Московской биржи.", font_style="Subtitle1",
                                     halign="center", size_hint_y=None, height=dp(50), theme_text_color="Secondary")
        layout.add_widget(self.message_label)
        layout.add_widget(MDLabel(text="Первый запуск — около 15 секунд. Далее данные из кэша мгновенно.",
                                  font_style="Caption", halign="center", size_hint_y=None, height=dp(40), theme_text_color="Secondary"))
        self.progress_bar = MDProgressBar(value=0, max=100, size_hint_y=None, height=dp(6),
                                          color=get_color_from_hex('#1565C0'))
        layout.add_widget(self.progress_bar)
        self.status_label = MDLabel(text="Подготовка...", font_style="Caption", halign="center", size_hint_y=None, height=dp(25),
                                    theme_text_color="Custom", text_color=get_color_from_hex('#616161'))
        layout.add_widget(self.status_label)
        self.skip_btn = MDFlatButton(text="Пропустить (использовать кэш)", font_style="Caption", halign="center",
                                     size_hint_y=None, height=dp(40), opacity=0,
                                     theme_text_color="Custom", text_color=get_color_from_hex('#1565C0'))
        self.skip_btn.bind(on_release=lambda x: self.finish_loading())
        layout.add_widget(self.skip_btn)
        layout.add_widget(Widget(size_hint_y=0.3))
        self.add_widget(layout)
    
    def update_progress(self, value, status_text=""):
        self.progress_bar.value = value
        if status_text: self.status_label.text = status_text
        if value > 30 and self.skip_btn.opacity == 0:
            Animation(opacity=1, duration=0.5).start(self.skip_btn)
    
    def finish_loading(self):
        self.app.show_main_interface()


# ==================== ПРИЛОЖЕНИЕ ====================

class BrokerApp(MDApp):
    def build(self):
        self.theme_cls.primary_palette = "Blue"
        self.theme_cls.theme_style = "Light"
        self.stocks_data = {s: {"name": STOCKS_INFO[s]["name"], "price": STOCKS_INFO[s]["price"]} for s in STOCKS_INFO}
        self.history_data = []
        self.orders = []
        self.moex_cache = load_cache()
        self.load_data()
        self.active_symbol = "SBER"
        self.all_stocks = []
        self.total_stocks = 0
        self.dialog = None
        self.manager_dialog = None
        self.orders_filter = "ALL"
        self._orders_mode = "ACTIVE"
        self.main_root = None
        self.loading_screen = LoadingScreen(self, name='loading')
        threading.Thread(target=self._background_load, daemon=True).start()
        return self.loading_screen
    
    def _background_load(self):
        Clock.schedule_once(lambda dt: self.loading_screen.update_progress(10, "Загружаем цены голубых фишек..."), 0)
        self._load_blue_chips()
        Clock.schedule_once(lambda dt: self.loading_screen.update_progress(33, "Цены загружены"), 0.2)
        Clock.schedule_once(lambda dt: self.loading_screen.update_progress(40, "Загружаем список акций..."), 0.3)
        all_stocks = get_moex_all_stocks()
        if all_stocks:
            seen = set()
            unique = []
            for s in all_stocks:
                if s['ticker'] not in seen:
                    seen.add(s['ticker'])
                    unique.append(s)
            self.all_stocks = unique
            self.total_stocks = len(unique)
            self.moex_cache['all_stocks'] = self.all_stocks
        Clock.schedule_once(lambda dt: self.loading_screen.update_progress(66, f"Найдено {self.total_stocks} акций"), 1)
        Clock.schedule_once(lambda dt: self.loading_screen.update_progress(75, "Загружаем цены биржи..."), 0.4)
        if self.all_stocks:
            for stock in self.all_stocks[:100]:
                if stock['ticker'] in BLUE_CHIPS: continue
                price = get_moex_price(stock['ticker'])
                if price and price > 0: stock['price'] = price
            self.moex_cache['all_stocks'] = self.all_stocks
        Clock.schedule_once(lambda dt: self.loading_screen.update_progress(90, "Цены загружены"), 1.5)
        Clock.schedule_once(lambda dt: self.loading_screen.update_progress(100, "Готово!"), 1.6)
        save_cache(self.moex_cache)
        Clock.schedule_once(lambda dt: self.loading_screen.finish_loading(), 2)
    
    def _load_blue_chips(self):
        for symbol in BLUE_CHIPS:
            if symbol not in STOCKS_INFO: continue
            cached = self.moex_cache.get(f"{symbol}_price")
            real_price = get_moex_price(symbol)
            if real_price and real_price > 0:
                self.stocks_data[symbol]['price'] = real_price
                STOCKS_INFO[symbol]['price'] = real_price
                self.moex_cache[f"{symbol}_price"] = real_price
                self.moex_cache[f"{symbol}_time"] = datetime.now().strftime("%Y-%m-%d %H:%M")
            elif cached:
                self.stocks_data[symbol]['price'] = cached
                STOCKS_INFO[symbol]['price'] = cached
    
    def show_main_interface(self):
        self.main_root = self._build_main_interface()
        self.root.clear_widgets()
        self.root.add_widget(self.main_root)
        self.refresh_ui()
        Clock.schedule_interval(self.refresh_prices, 300)
    
    def _build_main_interface(self):
        root = MDBoxLayout(orientation='vertical')
        self.toolbar = MDTopAppBar(
            title="Olimp Investing",
            anchor_title="center",
            right_action_items=[
                ["note-text", lambda x: self.show_orders_manager("ACTIVE")],
                ["clock-outline", lambda x: self.show_orders_manager("HISTORY")]
            ])
        root.add_widget(self.toolbar)
        nav = MDBottomNavigation()
        
        # ВИТРИНА
        showcase_item = MDBottomNavigationItem(name='screen_showcase', text='Витрина', icon='store')
        sc_layout = MDBoxLayout(orientation='vertical', padding=dp(15), spacing=dp(10))
        self.balance_label = MDLabel(text="", font_style="H5", halign="center", size_hint_y=None, height=dp(35),
                                     theme_text_color="Custom", text_color=get_color_from_hex('#212121'))
        sc_layout.add_widget(self.balance_label)
        sc_layout.add_widget(MDLabel(text="Голубые фишки", font_style="H6", halign="center", size_hint_y=None, height=dp(25),
                                     theme_text_color="Custom", text_color=get_color_from_hex('#1565C0')))
        stocks_grid = MDBoxLayout(orientation='vertical', spacing=dp(10), size_hint_y=None, height=dp(420))
        blue_chips = [s for s in BLUE_CHIPS if s in self.stocks_data]
        for row_start in range(0, len(blue_chips), 3):
            row = MDBoxLayout(orientation='horizontal', spacing=dp(10), size_hint_y=None, height=dp(135))
            for symbol in blue_chips[row_start:row_start + 3]:
                stock = self.stocks_data[symbol]
                info = STOCKS_INFO.get(symbol, {})
                card = MDCard(radius=[12], size_hint_x=1, md_bg_color=get_color_from_hex('#FFFFFF'),
                              line_color=get_color_from_hex('#E8E8E8'), elevation=2)
                card.bind(on_release=lambda x, s=symbol: self.show_stock_detail(s))
                cc = MDBoxLayout(orientation='vertical', padding=dp(10), spacing=dp(4))
                cc.add_widget(MDLabel(text=stock['name'], bold=True, font_style="Subtitle1", halign="center",
                                      size_hint_y=None, height=dp(22), theme_text_color="Custom", text_color=get_color_from_hex('#212121')))
                cc.add_widget(MDLabel(text=f"{stock['price']:.4f} ₽" if stock['price'] < 1 else f"{stock['price']:.1f} ₽",
                                      font_style="H6", halign="center", size_hint_y=None, height=dp(25),
                                      theme_text_color="Custom", text_color=get_color_from_hex('#1565C0')))
                sector = info.get('sector', '-')
                cc.add_widget(MDLabel(text=sector, font_style="Caption", halign="center", theme_text_color="Secondary", size_hint_y=None, height=dp(18)))
                card.add_widget(cc)
                row.add_widget(card)
            while len(row.children) < 3: row.add_widget(Widget())
            stocks_grid.add_widget(row)
        sc_layout.add_widget(stocks_grid)
        showcase_item.add_widget(sc_layout)
        
        # БИРЖА
        exchange_item = MDBottomNavigationItem(name='screen_exchange', text='Биржа', icon='chart-line')
        ex_layout = MDBoxLayout(orientation='vertical', spacing=dp(5))
        self.search_input = MDTextField(
            hint_text="Поиск по названию или тикеру...", mode="fill",
            size_hint_y=None, height=dp(50), padding=[dp(15), dp(10)])
        self.search_input.bind(text=self._on_search)
        ex_layout.add_widget(self.search_input)
        sector_scroll = ScrollView(size_hint_y=None, height=dp(40))
        self.sector_buttons = {}
        sector_row = MDBoxLayout(orientation='horizontal', spacing=dp(5), size_hint_x=None, padding=[dp(10), 0])
        sector_row.bind(minimum_width=sector_row.setter('width'))
        all_btn = MDFillRoundFlatButton(text="Все", size_hint_x=None, width=dp(60),
                                        md_bg_color=get_color_from_hex('#1565C0'))
        all_btn.bind(on_release=lambda x: self._filter_sector("Все"))
        sector_row.add_widget(all_btn)
        self.sector_buttons["Все"] = all_btn
        for sector in SECTORS.keys():
            btn = MDFillRoundFlatButton(text=sector, size_hint_x=None, width=dp(80),
                                        md_bg_color=get_color_from_hex('#E3F2FD'))
            btn.bind(on_release=lambda x, s=sector: self._filter_sector(s))
            sector_row.add_widget(btn)
            self.sector_buttons[sector] = btn
        sector_scroll.add_widget(sector_row)
        ex_layout.add_widget(sector_scroll)
        self.exchange_scroll = ScrollView()
        self.exchange_list = MDBoxLayout(orientation='vertical', size_hint_y=None, spacing=dp(2))
        self.exchange_list.bind(minimum_height=self.exchange_list.setter('height'))
        self.exchange_scroll.add_widget(self.exchange_list)
        ex_layout.add_widget(self.exchange_scroll)
        self.current_filter = "Все"
        self._update_exchange_list()
        exchange_item.add_widget(ex_layout)
        
        # ПОРТФЕЛЬ
        portfolio_item = MDBottomNavigationItem(name='screen_portfolio', text='Портфель', icon='briefcase')
        p_scroll = ScrollView()
        self.p_layout = MDBoxLayout(orientation='vertical', padding=dp(15), spacing=dp(10), size_hint_y=None)
        self.p_layout.bind(minimum_height=self.p_layout.setter('height'))
        self.summary_card = MDCard(size_hint_y=None, height=dp(130), padding=dp(15),
                                   md_bg_color=get_color_from_hex('#FFFFFF'), radius=[15], elevation=2)
        self.summary_layout = MDBoxLayout(orientation='vertical', spacing=dp(5))
        self.summary_layout.add_widget(MDLabel(text="Портфель", font_style="H5", halign="left", size_hint_y=None, height=dp(30),
                                               theme_text_color="Custom", text_color=get_color_from_hex('#1565C0')))
        self.balance_row = MDBoxLayout(orientation='horizontal', size_hint_y=None, height=dp(25))
        self.summary_balance_label = MDLabel(text="Баланс: 0 ₽", halign="left", font_style="Subtitle1",
                                             theme_text_color="Custom", text_color=get_color_from_hex('#212121'))
        self.summary_stocks_label = MDLabel(text="В акциях: 0 ₽", halign="right", font_style="Subtitle1",
                                            theme_text_color="Custom", text_color=get_color_from_hex('#212121'))
        self.balance_row.add_widget(self.summary_balance_label)
        self.balance_row.add_widget(self.summary_stocks_label)
        self.summary_layout.add_widget(self.balance_row)
        self.total_capital_label = MDLabel(text="Общий капитал: 0 ₽", halign="left", font_style="H6",
                                           theme_text_color="Custom", text_color=get_color_from_hex('#2E7D32'))
        self.summary_layout.add_widget(self.total_capital_label)
        self.summary_card.add_widget(self.summary_layout)
        self.p_layout.add_widget(self.summary_card)
        div_btn = MDRaisedButton(text="Мои дивиденды", md_bg_color=get_color_from_hex('#1565C0'),
                                 size_hint_y=None, height=dp(45), text_color=get_color_from_hex('#FFFFFF'))
        div_btn.bind(on_release=lambda x: MyDividendsDialog(self).show())
        self.p_layout.add_widget(div_btn)
        self.p_layout.add_widget(MDLabel(text="Активы", font_style="H6", halign="left", size_hint_y=None, height=dp(30),
                                         theme_text_color="Custom", text_color=get_color_from_hex('#1565C0')))
        self.assets_container = MDBoxLayout(orientation='vertical', spacing=dp(10), size_hint_y=None)
        self.assets_container.bind(minimum_height=self.assets_container.setter('height'))
        self.p_layout.add_widget(self.assets_container)
        p_scroll.add_widget(self.p_layout)
        portfolio_item.add_widget(p_scroll)
        
        nav.add_widget(showcase_item)
        nav.add_widget(exchange_item)
        nav.add_widget(portfolio_item)
        root.add_widget(nav)
        return root
    
    def get_stock_history(self, symbol):
        cached = self.moex_cache.get(f"{symbol}_history")
        if cached and len(cached) > 5: return cached
        backup = REAL_HISTORY_BACKUP.get(symbol)
        if backup:
            self.moex_cache[f"{symbol}_history"] = backup[:]
            save_cache(self.moex_cache)
            return backup
        return None
    
    def refresh_prices(self, dt):
        threading.Thread(target=self._load_blue_chips, daemon=True).start()
        Clock.schedule_once(lambda dt: self.refresh_ui(), 2)
    
    def show_stock_detail(self, symbol):
        self.active_symbol = symbol
        StockDetailDialog(self, symbol).show()
    
    def _update_exchange_list(self):
        self.exchange_list.clear_widgets()
        search_text = self.search_input.text.strip().lower() if self.search_input else ""
        filtered = []
        for stock in self.all_stocks:
            if self.current_filter != "Все" and stock.get('sector', 'Прочее') != self.current_filter: continue
            if search_text:
                if search_text not in stock['name'].lower() and search_text not in stock['ticker'].lower(): continue
            filtered.append(stock)
        filtered.sort(key=lambda x: POPULAR_TICKERS.get(x['ticker'], 999))
        for stock in filtered[:100]:
            price = stock.get('price', 0)
            card = MDCard(size_hint_y=None, height=dp(55), padding=dp(10),
                          md_bg_color=get_color_from_hex('#FFFFFF'), radius=[8], elevation=1)
            card.bind(on_release=lambda x, s=stock['ticker']: self.show_stock_detail(s))
            row = MDBoxLayout(orientation='horizontal')
            left = MDBoxLayout(orientation='vertical', size_hint_x=0.5)
            left.add_widget(MDLabel(text=stock['name'], bold=True, font_style="Subtitle1", theme_text_color="Custom", text_color=get_color_from_hex('#212121')))
            left.add_widget(MDLabel(text=f"{stock['ticker']}  {stock.get('sector', '-')}", font_style="Caption", theme_text_color="Secondary"))
            row.add_widget(left)
            right = MDBoxLayout(orientation='vertical', size_hint_x=0.5)
            if price > 0:
                if price < 1:
                    right.add_widget(MDLabel(text=f"{price:.4f} ₽", halign="right", bold=True, font_style="Subtitle1", theme_text_color="Custom", text_color=get_color_from_hex('#212121')))
                else:
                    right.add_widget(MDLabel(text=f"{price:.2f} ₽", halign="right", bold=True, font_style="Subtitle1", theme_text_color="Custom", text_color=get_color_from_hex('#212121')))
            else:
                right.add_widget(MDLabel(text="—", halign="right", bold=True, font_style="Subtitle1"))
            right.add_widget(MDLabel(text="", halign="right", font_style="Caption"))
            row.add_widget(right)
            card.add_widget(row)
            self.exchange_list.add_widget(card)
    
    def _on_search(self, instance, value):
        if hasattr(self, '_search_event'): Clock.unschedule(self._search_event)
        self._search_event = Clock.schedule_once(lambda dt: self._update_exchange_list(), 0.3)
    
    def _filter_sector(self, sector):
        self.current_filter = sector
        for s, btn in self.sector_buttons.items():
            btn.md_bg_color = get_color_from_hex('#1565C0') if s == sector else get_color_from_hex('#E3F2FD')
        self._update_exchange_list()
    
    def update_portfolio_tab(self):
        self.assets_container.clear_widgets()
        tsv = 0
        for s in list(self.stocks_data.keys()):
            d = self.portfolio.get(s, [0, 0.0])
            cnt = d[0] if isinstance(d, list) else 0
            cost = d[1] if isinstance(d, list) and len(d) > 1 else 0.0
            if cnt > 0: tsv += cnt * self.stocks_data[s]['price']
        tc = self.balance + tsv
        self.summary_balance_label.text = f"Баланс: {self.balance:,.0f} ₽".replace(',', ' ')
        self.summary_stocks_label.text = f"В акциях: {tsv:,.0f} ₽".replace(',', ' ')
        self.total_capital_label.text = f"Общий капитал: {tc:,.0f} ₽".replace(',', ' ')
        for s in list(self.stocks_data.keys()):
            d = self.portfolio.get(s, [0, 0.0])
            cnt = d[0] if isinstance(d, list) else 0
            cost = d[1] if isinstance(d, list) and len(d) > 1 else 0.0
            if cnt <= 0: continue
            cp = self.stocks_data[s]['price']
            avg = cost / cnt if cnt > 0 else 0
            cv = cnt * cp
            profit = cv - cost
            pp = (profit / cost * 100) if cost > 0 else 0
            card = MDCard(size_hint_y=None, height=dp(72), padding=dp(10),
                          md_bg_color=get_color_from_hex('#FFFFFF'), radius=[12], elevation=1)
            main_box = MDBoxLayout(orientation='horizontal', spacing=dp(8))
            ib = MDBoxLayout(orientation='vertical', size_hint_x=0.32)
            stock_name = STOCKS_INFO.get(s, {}).get('name', s)
            ib.add_widget(MDLabel(text=f"{stock_name}  {cnt} шт", bold=True, font_style="Subtitle1", theme_text_color="Custom", text_color=get_color_from_hex('#212121')))
            ib.add_widget(MDLabel(text=f"≈{avg:.4f} ₽" if avg < 1 else f"≈{avg:.0f} ₽", font_style="Caption", theme_text_color="Secondary"))
            main_box.add_widget(ib)
            main_box.add_widget(VerticalDivider())
            ab = MDBoxLayout(orientation='horizontal', size_hint_x=None, width=dp(70), spacing=dp(4), padding=[dp(5), 0])
            bb = MDFlatButton(text="+", font_style="H6", theme_text_color="Custom",
                              text_color=get_color_from_hex('#2E7D32'), size_hint_x=None, width=dp(36),
                              md_bg_color=get_color_from_hex('#E8F5E9'))
            bb.bind(on_release=lambda x, sym=s: self.open_trade_dialog(sym, "BUY"))
            ab.add_widget(bb)
            sb = MDFlatButton(text="−", font_style="H6", theme_text_color="Custom",
                              text_color=get_color_from_hex('#C62828'), size_hint_x=None, width=dp(36),
                              md_bg_color=get_color_from_hex('#FFEBEE'))
            sb.bind(on_release=lambda x, sym=s: self.open_trade_dialog(sym, "SELL"))
            ab.add_widget(sb)
            main_box.add_widget(ab)
            pb = MDBoxLayout(orientation='vertical', size_hint_x=0.38, padding=[dp(5), dp(8), 0, dp(8)])
            pc = get_color_from_hex('#2E7D32') if profit >= 0 else get_color_from_hex('#C62828')
            ps = "+" if profit >= 0 else ""
            pb.add_widget(MDLabel(text=f"{ps}{profit:,.0f}₽ ({pp:+.1f}%)".replace(',', ' '), halign="right",
                                  font_style="Caption", theme_text_color="Custom", text_color=pc))
            pb.add_widget(MDLabel(text=f"{cv:,.0f} ₽".replace(',', ' '), halign="right", bold=True, font_style="Subtitle1", theme_text_color="Custom", text_color=get_color_from_hex('#212121')))
            main_box.add_widget(pb)
            card.add_widget(main_box)
            self.assets_container.add_widget(card)
    
    def open_trade_dialog(self, symbol, side="BUY"):
        self.current_symbol = symbol
        self.current_side = side
        mp = self.stocks_data.get(symbol, {}).get('price', 100)
        lot = STOCKS_INFO.get(symbol, {}).get('lot', 1) if symbol in STOCKS_INFO else 1
        if lot == 1:
            for stock in self.all_stocks:
                if stock['ticker'] == symbol: lot = stock.get('lot', 1); break
        c = MDBoxLayout(orientation="vertical", spacing=dp(12), size_hint_y=None, height=dp(280))
        c.add_widget(MDLabel(text=f"Лот: {lot} шт. | Цена за лот: {mp * lot:,.2f} ₽", font_style="Caption", halign="center",
                              theme_text_color="Custom", text_color=get_color_from_hex('#616161'), size_hint_y=None, height=dp(25)))
        self.qty_input = MDTextField(hint_text=f"Количество лотов (1 лот = {lot} акций)", text="1", input_filter="int")
        self.prc_input = MDTextField(hint_text="Цена за 1 акцию", text=f"{mp:.4f}" if mp < 1 else f"{mp:.2f}")
        self.qty_input.bind(text=self.update_info_label)
        self.prc_input.bind(text=self.update_info_label)
        self.info_label = MDLabel(text="Реальная цена с MOEX", font_style="Caption", halign="center",
                                  theme_text_color="Custom", text_color=get_color_from_hex('#616161'))
        c.add_widget(self.qty_input); c.add_widget(self.prc_input); c.add_widget(self.info_label)
        color = get_color_from_hex('#2E7D32') if side=="BUY" else get_color_from_hex('#C62828')
        self.submit_btn = MDRaisedButton(text="ПОДТВЕРДИТЬ", md_bg_color=color)
        self.submit_btn.bind(on_release=lambda x: self.process_trade(side))
        self.dialog = MDDialog(title=f"{'Покупка' if side=='BUY' else 'Продажа'}: {symbol}", type="custom", content_cls=c,
                               buttons=[MDFlatButton(text="ОТМЕНА", on_release=lambda x: self.dialog.dismiss()), self.submit_btn])
        self.dialog.open(); Clock.schedule_once(lambda dt: self.update_info_label(), 0.1)
    
    def update_info_label(self, *args):
        try:
            q_lots = int(self.qty_input.text) if self.qty_input.text.isdigit() else 0
            p = float(self.prc_input.text.replace(',','.')) if self.prc_input.text else 0.0
            lot = STOCKS_INFO.get(self.current_symbol, {}).get('lot', 1) if self.current_symbol in STOCKS_INFO else 1
            if lot == 1:
                for stock in self.all_stocks:
                    if stock['ticker'] == self.current_symbol: lot = stock.get('lot', 1); break
            q = q_lots * lot
            if q<=0 or p<=0: self.info_label.text="Ошибка"; self.submit_btn.disabled=True; return
            is_buy = self.current_side=="BUY"; tv = q*p
            pd = self.portfolio.get(self.current_symbol, [0,0.0]); owned = pd[0] if isinstance(pd,list) else 0
            if is_buy:
                if tv>self.balance:
                    self.info_label.text=f"Недостаточно средств\n{q_lots} лот × {lot} шт × {p:.4f}₽ = {tv:,.2f} ₽\nДоступно: {self.balance:,.2f} ₽"
                    self.info_label.text_color=get_color_from_hex('#C62828'); self.submit_btn.disabled=True
                else:
                    self.info_label.text=f"{q_lots} лот × {lot} шт = {q} акций\nИтого: {tv:,.2f} ₽"
                    self.info_label.text_color=get_color_from_hex('#616161'); self.submit_btn.disabled=False
            else:
                if q>owned:
                    self.info_label.text=f"Недостаточно активов\nЗапрошено: {q} шт. | Доступно: {owned} шт."
                    self.info_label.text_color=get_color_from_hex('#C62828'); self.submit_btn.disabled=True
                else:
                    self.info_label.text=f"{q_lots} лот × {lot} шт = {q} акций\nВыручка: {tv:,.2f} ₽"
                    self.info_label.text_color=get_color_from_hex('#616161'); self.submit_btn.disabled=False
        except: self.submit_btn.disabled=True
    
    def process_trade(self, side):
        try:
            q=int(self.qty_input.text); p=float(self.prc_input.text.replace(',','.'))
            cp=self.stocks_data.get(self.current_symbol,{}).get('price',p)
            lot = STOCKS_INFO.get(self.current_symbol, {}).get('lot', 1) if self.current_symbol in STOCKS_INFO else 1
            q = q * lot
            if abs(p-cp)<p*0.02: self.execute_trade(self.current_symbol,side,q,p)
            else: self.orders.append({'symbol':self.current_symbol,'side':side,'price':p,'count':q}); self.save_data()
            self.dialog.dismiss()
        except: pass
    
    def execute_trade(self, symbol, side, q, p):
        try:
            if side=="BUY":
                if self.balance>=p*q:
                    self.balance-=p*q
                    od=self.portfolio.get(symbol,[0,0.0])
                    self.portfolio[symbol]=[(od[0] if isinstance(od,list) else 0)+q,(od[1] if isinstance(od,list) and len(od)>1 else 0.0)+p*q]
                    if symbol not in self.stocks_data: self.stocks_data[symbol]={"name":symbol,"price":p}
            else:
                od=self.portfolio.get(symbol,[0,0.0])
                owned=od[0] if isinstance(od,list) else 0
                cb=od[1] if isinstance(od,list) and len(od)>1 else 0.0
                qa=min(q,owned)
                if qa>0: self.balance+=p*qa; self.portfolio[symbol]=[owned-qa,cb-(cb/owned*qa)]
            self.history_data.append({'symbol':symbol,'side':side,'price':p,'count':q,'time':datetime.now().strftime("%H:%M:%S")})
            self.save_data(); self.refresh_ui()
        except: pass
    
    def refresh_ui(self):
        if hasattr(self, 'balance_label') and self.balance_label:
            self.balance_label.text = f"Баланс: {self.balance:,.2f} ₽".replace(',', ' ')
        if hasattr(self, 'assets_container'): self.update_portfolio_tab()
    
    def show_orders_manager(self, mode="ACTIVE"):
        self._orders_mode=mode
        c=MDBoxLayout(orientation="vertical",spacing=dp(8),size_hint_y=None,height=dp(480))
        h=MDBoxLayout(orientation='horizontal',size_hint_y=None,height=dp(40))
        ab=MDFlatButton(text="Активные"); hb=MDFlatButton(text="История")
        self._update_orders_header_style(ab,hb,mode)
        ab.bind(on_release=lambda x: self._switch_orders_mode("ACTIVE",ab,hb))
        hb.bind(on_release=lambda x: self._switch_orders_mode("HISTORY",ab,hb))
        h.add_widget(ab); h.add_widget(hb); c.add_widget(h)
        f=MDBoxLayout(orientation="horizontal",size_hint_y=None,height=dp(35),spacing=dp(5))
        for n,v in [("Все","ALL"),("Покупки","BUY"),("Продажи","SELL")]:
            btn=MDFlatButton(text=n); btn.bind(on_release=lambda x,fv=v: self._apply_orders_filter(fv)); f.add_widget(btn)
        c.add_widget(f)
        s=ScrollView(); self.orders_list_ui=MDList(); s.add_widget(self.orders_list_ui); c.add_widget(s)
        self.manager_dialog=MDDialog(title="Заявки",type="custom",content_cls=c,
                                     buttons=[MDFlatButton(text="ЗАКРЫТЬ",on_release=lambda x: self.manager_dialog.dismiss())])
        self._update_orders_list(); self.manager_dialog.open()
    
    def _update_orders_header_style(self,ab,hb,mode):
        if mode=="ACTIVE": ab.text_color, hb.text_color = get_color_from_hex('#1565C0'), get_color_from_hex('#616161')
        else: ab.text_color, hb.text_color = get_color_from_hex('#616161'), get_color_from_hex('#1565C0')
    
    def _switch_orders_mode(self,mode,ab,hb): self._orders_mode=mode; self._update_orders_header_style(ab,hb,mode); self._update_orders_list()
    def _apply_orders_filter(self,fv): self.orders_filter=fv; self._update_orders_list()
    
    def _update_orders_list(self):
        if not hasattr(self,'orders_list_ui'): return
        self.orders_list_ui.clear_widgets()
        src=self.orders if self._orders_mode=="ACTIVE" else self.history_data
        for item in reversed(src):
            if not isinstance(item,dict) or 'symbol' not in item: continue
            side=item.get('side','BUY')
            if self.orders_filter!="ALL" and side!=self.orders_filter: continue
            color=get_color_from_hex('#2E7D32') if side=="BUY" else get_color_from_hex('#C62828')
            txt=f"{item['symbol']} | {item['count']} шт. @ {item.get('price',0):.4f} ₽" if item.get('price',0)<1 else f"{item['symbol']} | {item['count']} шт. @ {item.get('price',0):.2f} ₽"
            if self._orders_mode!="ACTIVE": txt+=f" | {item.get('time','')}"
            ib=MDBoxLayout(orientation='horizontal',size_hint_y=None,height=dp(48),padding=[dp(10),dp(4)])
            ib.add_widget(MDLabel(text=txt,theme_text_color="Custom",text_color=color,size_hint_x=0.6))
            if self._orders_mode=="ACTIVE":
                ic={'symbol':item['symbol'],'side':side,'price':item.get('price',0),'count':item.get('count',0)}
                cb=MDFlatButton(text="✕",font_style="H6",theme_text_color="Custom",text_color=get_color_from_hex('#C62828'),size_hint_x=None,width=dp(36))
                cb.bind(on_release=lambda x,ic=ic: self.cancel_order_safe(ic)); ib.add_widget(cb)
                eb=MDFlatButton(text="✎",font_style="H6",theme_text_color="Custom",text_color=get_color_from_hex('#1565C0'),size_hint_x=None,width=dp(36))
                eb.bind(on_release=lambda x,ic=ic: self.edit_order(ic)); ib.add_widget(eb)
            self.orders_list_ui.add_widget(ib)
    
    def cancel_order_safe(self,oi):
        for o in self.orders[:]:
            if (o.get('symbol')==oi.get('symbol') and o.get('side')==oi.get('side') and 
                abs(o.get('price',0)-oi.get('price',0))<0.0001 and o.get('count')==oi.get('count')):
                self.orders.remove(o); self.save_data(); self._update_orders_list(); break
    
    def edit_order(self,oi):
        orig=next((o for o in self.orders[:] if 
                   o.get('symbol')==oi.get('symbol') and o.get('side')==oi.get('side') and 
                   abs(o.get('price',0)-oi.get('price',0))<0.0001 and o.get('count')==oi.get('count')),None)
        if not orig: return
        self.orders.remove(orig); self.manager_dialog.dismiss()
        self.current_symbol=orig['symbol']; self.current_side=orig['side']
        c=MDBoxLayout(orientation="vertical",spacing=dp(12),size_hint_y=None,height=dp(280))
        c.add_widget(MDLabel(text=f"Изменение {orig['symbol']}",font_style="Subtitle1",halign="center",size_hint_y=None,height=dp(30)))
        self.qty_input=MDTextField(hint_text="Кол-во (акций)",text=str(orig['count']),input_filter="int")
        self.prc_input=MDTextField(hint_text="Цена",text=f"{orig['price']:.4f}" if orig['price']<1 else f"{orig['price']:.2f}")
        self.qty_input.bind(text=self.update_info_label); self.prc_input.bind(text=self.update_info_label)
        self.info_label=MDLabel(text="Параметры",font_style="Caption",halign="center",theme_text_color="Custom",text_color=get_color_from_hex('#616161'))
        c.add_widget(self.qty_input); c.add_widget(self.prc_input); c.add_widget(self.info_label)
        self.submit_btn=MDRaisedButton(text="Сохранить",md_bg_color=get_color_from_hex('#1565C0'))
        self.submit_btn.bind(on_release=lambda x: self.update_existing_order(orig['side']))
        self.dialog=MDDialog(title=f"Изменение: {orig['symbol']}",type="custom",content_cls=c,
                             buttons=[MDFlatButton(text="Отмена",on_release=lambda x: (self.orders.append(orig),self.save_data(),self.dialog.dismiss())),self.submit_btn])
        self.dialog.open(); Clock.schedule_once(lambda dt: self.update_info_label(),0.1)
    
    def update_existing_order(self,side):
        try:
            q=int(self.qty_input.text); p=float(self.prc_input.text.replace(',','.'))
            if q<=0 or p<=0: return
            self.orders.append({'symbol':self.current_symbol,'side':side,'price':p,'count':q})
            self.save_data(); self.dialog.dismiss(); self.show_orders_manager(self._orders_mode)
        except: pass
    
    def load_data(self):
        if os.path.exists('broker_data.json'):
            try:
                with open('broker_data.json','r',encoding='utf-8') as f:
                    d=json.load(f)
                    self.balance=d.get('balance',1000000)
                    self.portfolio=d.get('portfolio',{})
                    self.orders=d.get('orders',[])
                    self.history_data=d.get('history',[])
            except: self.reset_data()
        else: self.reset_data()
        for s in list(self.stocks_data.keys()):
            if s not in self.portfolio: self.portfolio[s]=[0,0.0]
    
    def save_data(self):
        try:
            with open('broker_data.json','w',encoding='utf-8') as f:
                json.dump({'balance':self.balance,'portfolio':self.portfolio,'orders':self.orders,'history':self.history_data},f,ensure_ascii=False,indent=2)
        except: pass
    
    def reset_data(self):
        self.balance=1_000_000
        self.portfolio={s:[0,0.0] for s in self.stocks_data}
        self.orders=[]; self.history_data=[]


if __name__ == "__main__":
    BrokerApp().run()