"""
The main file, where all the other files are combined into a (hopefully) meaningful output
Uses argparse to interface nicely with the command prompt
"""

import argparse
from image import Mandelbrot_BW

def main():
    parser = argparse.ArgumentParser(description="Fractal image generator for Julia sets")
    subparsers = parser.add_subparsers(dest='command', required=True)

    mandelbrot_bw_parser = subparsers.add_parser("Mandelbrot_BW", help="Generate a pure black and white mandelbrot image.")
    mandelbrot_bw_parser.add_argument("complex_min", type=complex, help="Complex number representing the bottom left corner of the image")
    mandelbrot_bw_parser.add_argument("complex_max", type=complex, help="Complex number representing the top right corner of the image")
    mandelbrot_bw_parser.add_argument("max_iter", type=int, help="Maximum number of iterations")
    mandelbrot_bw_parser.add_argument("-n", "--name", default="Mandelbrot_BW", help="Output file name, no file extension needed")

    args = parser.parse_args()

    if args.command == "Mandelbrot_BW":
        print("Starting image generation...")
        Mandelbrot_BW(args.complex_min, args.complex_max, args.max_iter, args.name)
        print("...image generation finished.")
    else:
        print("Something went wrong")

if __name__ == "__main__":
    main()
