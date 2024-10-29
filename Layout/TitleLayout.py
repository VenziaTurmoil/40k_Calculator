from dash import html

from Layout.AbstractLayout import AbstractLayout

class TitleLayout(AbstractLayout):
    
    def buildLayout(self):
        return html.Div(html.H1('40k_Calculator'),
                className='d-flex justify-content-center')
    
    def buildCallbacks(self):
        return True