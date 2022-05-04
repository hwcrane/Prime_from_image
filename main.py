import os
import sys
import time
from PIL import Image, ImageOps, ImageEnhance
import numpy as np
import subprocess
from threading import Thread
from primes import generate_possible_primes, to_digit

# WIDTH = 167
# HEIGHT = 83


class Main:
    def __init__(self, arguments: list[str]) -> None:
        self.threads: list[Thread] = []
        self.threads_running: int = 0
        self.prime_found: np.array | None = None
        self.base_image: np.array = None
        self.possible_primes: list[str] = []
        self.current_thread: int = 0
        self.start_time: float = time.time()
        self.interpret_arguments(arguments)

    def interpret_arguments(self, arguments: list[str]) -> None:
        '''
        Loads the image paths and dimentions from the program arguments
        '''

        # Input Image
        self.image_path: str = arguments[
            arguments.index('-i') + 1]

        # Output file
        self.output_file: str = arguments[
            arguments.index('-o') + 1]

        # Width
        self.width: int = int(arguments[
            arguments.index('-w') + 1])

        # Height
        self.height: int = int(arguments[
            arguments.index('-h') + 1])

    def setup(self) -> None:
        '''
        Loads image from file, converts it to numpy array, generates possible primes
        '''

        # Load Image
        image = Image.open(
            f"./{self.image_path}").resize((self.width, self.height))
        gray = ImageOps.grayscale(image)
        gray = ImageEnhance.Contrast(gray).enhance(1.7)

        # Convert image to numpy array
        array = np.asarray(gray)
        self.base_image = np.vectorize(to_digit)(array)

        print('generating possible primes')

        # Generate possible primes
        self.possible_primes = generate_possible_primes(self.base_image, 1000)

    def mainloop(self):
        '''
        Program Mainloop
        '''

        while self.prime_found == None:

            # Prints status to console
            os.system('clear')
            print(
                f'Possiblities Tried: {self.current_thread - self.threads_running}')
            print(f'Threads running: {self.threads_running}')
            print(f'Time running: {round(time.time() - self.start_time)}s)')

            # If no possible primes left, generates new ones
            if self.current_thread == len(self.possible_primes) and self.threads_running == 0:
                self.possible_primes = generate_possible_primes(
                    self.base_image, 1000, set(self.possible_primes))

            # Generates new threads if number running drops below 100
            while self.threads_running < 100 and self.current_thread < len(self.possible_primes):
                self.start_thread(self.possible_primes[self.current_thread])
                self.current_thread += 1

            time.sleep(0.5)

        self.save_image()

    def start_thread(self, prime: str):
        '''
        Starts a new thread and appends it to the threads list
        '''

        thread = Thread(target=self.checkPrime,
                        args=(prime, ))
        thread.start()
        self.threads.append(thread)

    def checkPrime(self, number: str):
        '''
        Checks if number is prime
        '''

        self.threads_running += 1
        if str(subprocess.run(['openssl', 'prime', number], capture_output=True).stdout).endswith('is prime\\n\''):
            self.prime_found = number
            print('prime found')
        self.threads_running -= 1

    def save_image(self):
        '''
        Saves found prime to file
        '''

        if self.prime_found is not None:
            with open(f'{self.output_file}.txt', 'w') as file:
                for j in range(self.height):
                    file.write(
                        self.prime_found[j * self.width: (j + 1) * self.width])
                    file.write('\n')


if __name__ == '__main__':
    app = Main(sys.argv)
    app.setup()
    app.mainloop()
