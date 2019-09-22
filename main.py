from Audio import Audio

def main():
    a = Audio()
    for w in a.recognize():
        if w == "Sending":
            print("Sending...")
        elif w == "Listening":
            print("Listening...")

        print(w)

if __name__ == "__main__":
    main()