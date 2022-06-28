def main():
    # Welcome message
    print("Parses and downloads manga from websites with online viewing")

    # Ask some questions

    # Ask website from each will download manga
    print("Choose manga website from domain name list:")

    # Define a domains dict
    domains = {1: "mangalib.me"}

    for key, value in domains.items():
        print(f'[{key}] {value}')

    url_key = int(input())

    print(domains[url_key])

    match domains[url_key]:
        case "mangalib.me":
            from websites_modules import mangalib_me
        case _:
            print("Something went wrong")


if __name__ == "__main__":
    main()
