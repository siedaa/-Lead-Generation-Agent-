from agent.email_finder import find_email

urls = [
    "https://gloriajeanscoffees.com.pk/",
    "https://www.avari.com/property/beach-luxury",
    "https://this-does-not-exist-12345.com",
]

for url in urls:
    result = find_email(url)
    print(f"URL: {url}")
    print(f"Email: {result!r}\n")
