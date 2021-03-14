'''
Usage: display_pi [--palette COLORS] [--num-digits N] [--width W] [--height H] [--help] [--version]

Options:
    --palette COLORS    where COLORS is a comma separated list of color names representing digits 0-9 [default: purple,violet,blue,lightblue,green,yellow,orange,red,crimson,black]
    --num-digits N      the number of digits of PI to display [default: 1000]

    --width W           the width of the display [default: 640]
    --height H          the height of the display [default: 640]

    --help              display this help text and exit
    --version           display version and exit
'''
from math import pi, isqrt, sqrt

from docopt import docopt
from guizero import App, Waffle


def pi_digit_generator():
    '''from https://stackoverflow.com/questions/9004789/1000-digits-of-pi-in-python'''
    q, r, t, k, m, x = 1, 0, 1, 1, 3, 3
    for j in range(1000):
        if 4 * q + r - t < m * t:
            yield m
            q, r, t, k, m, x = 10*q, 10*(r-m*t), t, k, (10*(3*q+r))//t - 10*m, x
        else:
            q, r, t, k, m, x = q*k, (2*q+r)*x, t*x, k+1, (q*(7*k+2)+r*x)//(t*x), x+2


def validate_digits(n):
    '''Must be of form isqrt(n) ** 2'''
    root_n = isqrt(n)
    root_n = root_n + 1 if root_n < sqrt(n) else root_n
    return root_n ** 2


class PiDisplayAdapter:
    def __init__(self, opts):
        self.palette = [c for c in opts['--palette'].split(',')]
        self.num_digits = validate_digits(int(opts['--num-digits']))

        self.size = isqrt(self.num_digits)

        self.width = int(opts['--width'])
        self.height = int(opts['--height'])

    def display_pi(self):
        app = App(f'Happy PI day! {self.num_digits} digits of PI', self.width, self.height)
        canvas = Waffle(app, width=self.size, height=self.size, pad=0)

        self.fill_with_digits(canvas)

        app.display()

    def fill_with_digits(self, canvas):
        digits = self.pi_digits()

        for y in range(self.size):
            for x in range(self.size):
                digit = next(digits)
                # print(f'digit={digit}')
                color = self.palette[digit]
                # print(f'color={color}')
                canvas.set_pixel(x, y, color)

    def pi_digits(self):
        while True:
            for d in pi_digit_generator():
                yield int(d)


def display_pi(opts):
    adapter = PiDisplayAdapter(opts)
    adapter.display_pi()


if __name__ == '__main__':
    opts = docopt(__doc__, version=str(pi))
    print(opts)

    display_pi(opts)
