# HTMLFormParser v0.1
#
# (C) Kurtis Dipo aka Piotr Dusik 2012
# http://piotr.dusik.pl
# piotr@dusik.pl
#

class TagParser:
    tag,  key, quot, value = "", "", "", ""
    items = {}
    equals = False
    inside_tag = 0
    
    def parse(self, data):
        parser = {"'" : self.quote,
                  '"' : self.quote,
                  "=" : self.eq,
                  " " : self.whitespace,
                  "<" : self.tag_open,
                  ">" : self.tag_close,
                  "\n": self.whitespace}
       
        self.i = 0
        self.data = data

        for c in data:
            self.i += 1
            if c in parser:
                if parser[c](c) is True: 
                    break
            else:
                self.other_chars(c)
     
        ret =  {"tag": self.tag, "items": self.items, "offset": self.i}
        self.clear_vars()
        return ret

    def quote(self, c):
        if self.inside_tag == 2 and  self.key and self.equals:
            if self.quot == c:
                self.items[self.key] = self.value
                self.key, self.value, self.quot, self.equals = "", "", "", False
            elif self.quot == "":
                self.quot = c
            else:
               self.value += c
    
    def eq(self, c):
        if self.key and self.value == "":
            self.equals = True
        elif self.quot:
            self.value += c

    def other_chars(self, c):
        if self.inside_tag == 2:
            if self.quot != "":
                self.value += c
            else:
                self.key += c
        elif self.inside_tag == 1:
            self.tag += c

    def whitespace(self, c):
        if self.quot:
            self.value += c
        elif self.inside_tag == 1:
            self.inside_tag = 2

    def tag_open(self, c):
        if not self.quot and self.inside_tag is 0:
            self.inside_tag = 1
        elif self.quot:
            self.value += c       

    def tag_close(self, c):
        if self.inside_tag > 0 and not self.quot:
            return True

    def clear_vars(self):
        self.inside_tag = 0
        self.quot = ""
        self.items = {}
        self.value = ""
        self.equals = False
        self.key = ""
        self.tag = ""

class HTMLFormParser:
    items = {}    
    action = ""
    form_identifier = {}

    def set_form_identifier(self, ident):
        """
        Set form identificator ie. {"id" : "form_id"} or {"name" : "form_name"}
 
        :param ident: Dictionary containing one entry 
        """
        if not isinstance(ident, dict) or len(ident) is not 1:
            raise Exception("Bad param ident.")
         
        self.form_identifier = ident

    def parse(self, data):
        """
        Parse given by user input

        :param data: String buffer containing HTML code for parser
        """

        parser = TagParser()
        found_form = False

        while len(data) > 0:
            res = parser.parse(data)
            if found_form:
                if res["tag"] == "/form":
                    found_form = False
                elif "name" in res["items"] and "value" in res["items"]:
                    self.items[res["items"]["name"]] = res["items"]["value"]
            elif res["tag"] == "form":
                if len(self.form_identifier) == 1:
                    key, val = self.form_identifier.items()[0]
                else:
                    raise ValueError("Empty form_identifier")

                if key in res["items"] and res["items"][key] == val:
                    found_form = True
                    self.action = res["items"]["action"]

            data = data[res["offset"]:]
