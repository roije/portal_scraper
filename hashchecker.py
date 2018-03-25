import hashlib

class HashChecker():

    def __init__(self):
        self.hashfile = 'prev_hash.txt'
        self.prev_hash = None
        self.current_hash = None

    def generate_hash(self, comment_items):
        latest_comment = comment_items[0]

        # Remote comment time span
        post_date = latest_comment.find('span', class_='comment_profilepostdate')
        post_date.decompose()

        latest_comment_hash = hashlib.md5(str(latest_comment).encode("utf-8"))
        self.current_hash = latest_comment_hash

    def hash_compare(self):
        """
            Compares current hash with hash saved in file 
            Returns: boolean
        """
        prev_hash = self.get_prev_hash()
        if prev_hash:
            print(self.prev_hash)
            print(self.current_hash.hexdigest())
            if self.prev_hash == self.current_hash.hexdigest():
                print("Page unchanged. Return False")
                return False
            else:
                print("Page has changed. Return True")
                return True
        else:
            print("No hash to compare with. Return True")
            return True

    def save_new_hash(self):
        with open(self.hashfile, 'w', encoding='utf-8') as file_object:
            file_object.write(self.current_hash.hexdigest())
    
    def get_prev_hash(self):
        try:
            with open(self.hashfile, 'r', encoding='utf-8') as file_object:
                self.prev_hash = file_object.read()
        except FileNotFoundError:
             print("No hash file.")
        return self.prev_hash