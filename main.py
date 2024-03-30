from src.cha import ChaData

def main():
    data = ChaData("input/BWL_2002_3Bags_iPad_reading.cha")
    print(data.utterances)


if __name__ == "__main__":
    main()
