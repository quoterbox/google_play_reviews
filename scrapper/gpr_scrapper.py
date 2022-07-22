
class GPRScrapper:



    def clear_string(string: str) -> str:
        special_characters = [";", "\t", "\n", "\r", "\n\r", "<", ">"]
        return ''.join(filter(lambda i: i not in special_characters, string)).strip()

