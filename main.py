import random
import math
from kivy.app import App
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.graphics import Color, Rectangle, Line, Ellipse
from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout

# Android/Kivy conversion of Calculus Jetpack.
# Landscape game area; tap/hold the play area to fly upward.

def mono(c, n):
    if n == 0: return str(c)
    return ("" if c == 1 else str(c)) + ("x" if n == 1 else f"x^{n}")

def poly(terms):
    out = ""
    for i, (c, n) in enumerate(terms):
        if not c: continue
        body = mono(abs(c), n)
        if not out: out = ("-" if c < 0 else "") + body
        else: out += (" - " if c < 0 else " + ") + body
    return out or "0"

def easy_q():
    t = random.choice([1, 2, 3])
    hint = "Power rule: d/dx x^n = n x^(n-1)"
    if t == 1:
        a, n = random.randint(2, 9), random.randint(2, 5)
        return (f"d/dx [ {mono(a,n)} ]", mono(a*n,n-1),
                [mono(a,n-1), mono(a*n,n), mono(a*(n-1),n-1), mono(n,n-1)], hint)
    if t == 2:
        n, m = random.sample([2,3,4,5], 2)
        a, b = random.randint(2,7), random.randint(2,7)
        return (f"d/dx [ {poly([(a,n),(b,m)])} ]",
                poly([(a*n,n-1),(b*m,m-1)]),
                [poly([(a,n-1),(b,m-1)]), poly([(a*n,n-1),(b,m)]),
                 poly([(a*n,n-1),(b,m-1)]) + " + 1"],
                hint + "; differentiate term by term")
    a, n, k = random.randint(2,8), random.randint(2,5), random.randint(2,20)
    return (f"d/dx [ {poly([(a,n),(k,0)])} ]", mono(a*n,n-1),
            [poly([(a*n,n-1),(k,0)]), poly([(a,n-1),(k,0)]), mono(a*n,n)],
            "Derivative of a constant is 0")

def medium_q():
    t = random.choice(range(6))
    if t == 0:
        a=random.randint(2,9); return (f"d/dx [ {a} sin x ]",f"{a} cos x",
            [f"-{a} cos x",f"{a} sin x","cos x",f"-{a} sin x"],"d/dx sin x = cos x")
    if t == 1:
        a=random.randint(2,9); return (f"d/dx [ {a} cos x ]",f"-{a} sin x",
            [f"{a} sin x",f"-{a} cos x","-sin x",f"{a} cos x"],"d/dx cos x = -sin x")
    if t == 2:
        k=random.randint(2,7); return (f"d/dx [ e^({k}x) ]",f"{k}e^({k}x)",
            [f"e^({k}x)",f"e^({k}x) / {k}",f"{k}x e^({k}x - 1)"],"Chain rule")
    if t == 3:
        a=random.randint(2,9); return (f"d/dx [ {a} ln x ]",f"{a} / x",
            [f"1 / ({a}x)",f"{a} ln x / x",f"{a}x","1 / x"],"d/dx ln x = 1/x")
    if t == 4:
        a,b,n=random.randint(2,5),random.randint(1,9),random.randint(2,4)
        base=f"({a}x + {b})"; pw="" if n-1==1 else f"^{n-1}"
        return (f"d/dx [ {base}^{n} ]",f"{a*n}{base}{pw}",
            [f"{n}{base}{pw}",f"{a}{base}{pw}",f"{a*n}{base}^{n}"],"Chain rule")
    n=random.randint(2,4)
    return (f"d/dx [ {mono(1,n)} e^x ]",f"{mono(n,n-1)} e^x + {mono(1,n)} e^x",
            [f"{mono(n,n-1)} e^x",f"{mono(1,n)} e^x",f"{mono(n,n-1)} e^x - {mono(1,n)} e^x"],"Product rule")

def hard_q():
    t=random.choice(range(6))
    if t==0:
        n=random.randint(2,4)
        return (f"d/dx [ {mono(1,n)} sin x ]",f"{mono(n,n-1)} sin x + {mono(1,n)} cos x",
            [f"{mono(n,n-1)} cos x",f"{mono(1,n)} cos x",f"{mono(n,n-1)} sin x - {mono(1,n)} cos x"],"Product rule")
    if t==1:
        a=random.randint(2,5)
        return (f"d/dx [ sin({a}x^2) ]",f"{2*a}x cos({a}x^2)",
            [f"cos({a}x^2)",f"-{2*a}x cos({a}x^2)",f"{2*a}x sin({a}x^2)"],"Chain rule")
    if t==2:
        return ("d/dx [ e^x / x ]","e^x (x - 1) / x^2",
            ["e^x / x^2","e^x (x + 1) / x^2","e^x (1 - x) / x^2"],"Quotient rule")
    if t==3:
        a=random.randint(1,9)
        return (f"d/dx [ ln(x^2 + {a}) ]",f"2x / (x^2 + {a})",
            [f"1 / (x^2 + {a})",f"2x ln(x^2 + {a})",f"(x^2 + {a}) / 2x"],"Chain rule")
    if t==4:
        c=random.randint(2,9)
        return (f"d/dx [ x / (x + {c}) ]",f"{c} / (x + {c})^2",
            [f"1 / (x + {c})^2",f"-{c} / (x + {c})^2",f"{c} / (x + {c})"],"Quotient rule")
    a=random.randint(2,4)
    return (f"d/dx [ e^(x^{a}) ]",f"{a}x^{a-1} e^(x^{a})" if a>2 else "2x e^(x^2)",
            [f"e^(x^{a})",f"x^{a} e^(x^{a} - 1)",f"{a}x^{a-1} e^({a}x)"],"Chain rule")

GENERATORS={"EASY":easy_q,"MEDIUM":medium_q,"HARD":hard_q}
SETTINGS={"EASY":(250,2.0,15.0),"MEDIUM":(290,1.35,12.0),"HARD":(330,1.05,11.0)}

class JetpackGame(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.mode="menu"; self.diff="EASY"
        self.bind(size=self.redraw, pos=self.redraw)
        self.reset_game()
        Clock.schedule_interval(self.update, 1/60)

    def reset_game(self):
        self.speed0,self.z_int,self.g_int=SETTINGS[self.diff]
        self.speed=self.speed0; self.player_y=.5; self.vy=0
        self.score=0; self.lives=3; self.correct_count=0
        self.zappers=[]; self.gate=None; self.z_timer=1.0; self.g_timer=6.0
        self.held=False; self.message=""; self.message_time=0
        self.question=None; self.answers=[]; self.correct_index=0
        self.gate_x=1.2

    def start(self, diff):
        self.diff=diff; self.reset_game(); self.mode="play"

    def new_question(self):
        q, correct, wrongs, hint=GENERATORS[self.diff]()
        opts=[]
        for item in wrongs:
            if item != correct and item not in opts: opts.append(item)
        opts=opts[:2]
        while len(opts)<2: opts.append(correct+" + 1")
        opts.append(correct); random.shuffle(opts)
        self.question=q; self.answers=opts; self.correct_index=opts.index(correct)
        self.hint=hint

    def hit(self):
        self.lives-=1
        if self.lives<=0:
            self.mode="over"; self.held=False

    def update(self, dt):
        if self.mode!="play": self.redraw(); return
        dt=min(dt,.05)
        self.speed=self.speed0+self.score/40
        obstacle_speed=self.speed*(.85 if self.diff=="EASY" else 1.0)
        self.vy += (-1.65 if self.held else 1.05)*dt
        self.vy=max(-.48,min(.48,self.vy))
        self.player_y=max(.08,min(.90,self.player_y+self.vy*dt))
        self.score += self.speed*dt/10
        self.message_time=max(0,self.message_time-dt)
        if self.gate is None:
            self.z_timer-=dt; self.g_timer-=dt
            if self.z_timer<=0:
                self.z_timer=self.z_int*random.uniform(.8,1.3)
                self.zappers.append([1.05,random.uniform(.12,.78),random.uniform(.18,.38)])
            if self.g_timer<=0:
                self.g_timer=self.g_int; self.new_question()
                self.gate=[1.25,False]
        for z in self.zappers: z[0]-=obstacle_speed*dt/650
        self.zappers=[z for z in self.zappers if z[0]>-.08]
        px=.17; py=self.player_y
        for z in self.zappers:
            if abs(z[0]-px)<.035 and z[1]-.04<py<z[1]+z[2]+.04:
                self.hit(); z[0]=-1
        if self.gate:
            self.gate[0]-=obstacle_speed*dt/650
            if not self.gate[1] and self.gate[0]<.205:
                self.gate[1]=True
                lane=min(2,max(0,int((1-self.player_y)*3)))
                if lane==self.correct_index:
                    self.score+=100; self.correct_count+=1
                    self.message="TAMA! +100 | "+self.hint
                else:
                    self.message="MALI! Sagot: "+self.answers[self.correct_index]
                    self.hit()
                self.message_time=3
            if self.gate[0]<-.5: self.gate=None; self.z_timer=1.2
        self.redraw()

    def on_touch_down(self,touch):
        if not self.collide_point(*touch.pos): return super().on_touch_down(touch)
        if self.mode=="play":
            self.held=True
            # Tap one of the three answer lanes while gate is approaching.
            return True
        return super().on_touch_down(touch)

    def on_touch_up(self,touch):
        self.held=False
        return super().on_touch_up(touch)

    def choose(self, diff):
        self.start(diff)

    def draw_text(self, text, x, y, size=18, color=(1,1,1,1), halign="center"):
        lbl=Label(text=text, font_size=size, color=color, size_hint=(None,None),
                  size=(self.width*.92, max(30,size*2)), pos=(x-self.width*.46,y-size))
        lbl.text_size=lbl.size; lbl.halign=halign
        self.add_widget(lbl)

    def redraw(self,*args):
        self.clear_widgets()
        self.canvas.clear()
        w,h=self.width,self.height
        if w<=1 or h<=1: return
        with self.canvas:
            Color(.055,.07,.16,1); Rectangle(pos=self.pos,size=self.size)
            Color(.22,.26,.43,1); Rectangle(pos=(0,h*.08),size=(w,h*.06)); Rectangle(pos=(0,h*.88),size=(w,h*.06))
            Color(.45,.5,.75,1); Line(points=[0,h*.14,w,h*.14],width=1); Line(points=[0,h*.88,w,h*.88],width=1)
            if self.mode=="play":
                # player
                Color(.9,.9,.95,1); Rectangle(pos=(w*.14,h*self.player_y),size=(w*.035,h*.075))
                Color(.25,.65,1,1); Rectangle(pos=(w*.155,h*(self.player_y+.035)),size=(w*.017,h*.02))
                # zappers
                for x,y,hh in self.zappers:
                    Color(1,.85,.15,1); Line(points=[w*x,h*y,w*x,h*(y+hh)],width=4)
                # gate with three answer lanes
                if self.gate:
                    gx=self.gate[0]
                    lane_h=h*.74/3
                    cols=[(.85,.3,.3,1),(.25,.75,.45,1),(.3,.5,.9,1)]
                    for i in range(3):
                        Color(*cols[i]); Rectangle(pos=(w*(gx-.12),h*.14+i*lane_h),size=(w*.24,lane_h))
                # score/status text
        if self.mode=="menu":
            self.draw_text("CALCULUS JETPACK",w*.5,h*.72,32,(1,.9,.35,1))
            self.draw_text("Pumili ng difficulty",w*.5,h*.60,20)
            for i,d in enumerate(("EASY","MEDIUM","HARD")):
                b=Button(text=d,size_hint=(None,None),size=(w*.55,h*.09),pos=(w*.225,h*(.43-i*.12)))
                b.bind(on_release=lambda inst,level=d:self.choose(level)); self.add_widget(b)
        elif self.mode=="play":
            self.draw_text(f"{self.diff}   Score: {int(self.score)}   Buhay: {self.lives}   Tama: {self.correct_count}",w*.5,h*.94,16)
            if self.gate and self.question:
                self.draw_text(self.question,w*.5,h*.83,20,(1,.93,.55,1))
                for i,a in enumerate(self.answers):
                    self.draw_text(f"{i+1}. {a}",w*.5,h*(.72-i*.19),17)
            if self.message_time>0: self.draw_text(self.message,w*.5,h*.03,14,(.5,1,.6,1))
            self.draw_text("HOLD screen = fly up | Release = fall",w*.5,h*.005,12,(.7,.75,.9,1))
        else:
            self.draw_text("GAME OVER",w*.5,h*.65,34,(1,.35,.35,1))
            self.draw_text(f"Score: {int(self.score)}   Tamang sagot: {self.correct_count}",w*.5,h*.52,20)
            b=Button(text="PLAY AGAIN",size_hint=(None,None),size=(w*.55,h*.1),pos=(w*.225,h*.32))
            b.bind(on_release=lambda *_:self.start(self.diff)); self.add_widget(b)
            b2=Button(text="MENU",size_hint=(None,None),size=(w*.55,h*.1),pos=(w*.225,h*.18))
            b2.bind(on_release=lambda *_:setattr(self,"mode","menu") or self.redraw()); self.add_widget(b2)

class CalculusJetpackApp(App):
    def build(self):
        Window.clearcolor=(.055,.07,.16,1)
        Window.size=(960,540)
        Window.fullscreen="auto"
        return JetpackGame()

if __name__=="__main__":
    CalculusJetpackApp().run()
