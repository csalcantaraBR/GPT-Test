def test_addition():
    from pages.desktop.calculator_page import CalculatorPage
    calc = CalculatorPage()
    calc.open()
    calc.press(2)
    calc.press('+')
    calc.press(3)
    calc.press('=')
    assert calc.read_result() == 5
    calc.close()
