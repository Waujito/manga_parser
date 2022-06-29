from pathlib import Path


def main():
    # Welcome message
    print("Parses and downloads manga from websites with online viewing")
    print(
        f"Parsed manga will locate in {Path(__file__).parent.joinpath('dist_manga').resolve().absolute()}")

    # Ask some questions

    # Ask website from each will download manga
    print("Choose manga website from domain name list:")

    # Define a domains dict
    domains = {1: "mangalib.me"}

    for key, value in domains.items():
        print(f'[{key}] {value}')

    url_key = int(input())

    match domains[url_key]:
        case "mangalib.me":
            print(f"Starting {domains[url_key]} module")
            from websites_modules import mangalib_me
            mangalib_me.execute()
        case _:
            print("Something went wrong")


if __name__ == "__main__":
    main()
