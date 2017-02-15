from pymongo import MongoClient


class DataBaseManager(object):

    COL_NAME_SET = ['id', 'name', 'age', 'sex', 'salary']

    def __init__(self):
        client = MongoClient()
        database = client.people
        self.col = database.personal_info
        #Python的函数是可以直接通过字典来传递的,因此使用这种方法可以减少很多不必要的if判断。
        self.method_dict = {'add': self.add_person_info,
                            'update': self.update_person_info,
                            'del': self.del_person_info,
                            'show': self.show_person_info,
                            'help': self.show_help,
                            'exit': exit}
        self.run()

    def run(self):
        '''
        启动一个循环，使程序一直运行，直到输入exit为止。
        在循环中，接收输入并分析输入的命令，从而进行相应的操作。
        '''
        command = 'help'
        while command != 'exit':
            command = self.getInput()
            self.analysis(command)

    def getInput(self):
        '''
        获取输入的信息。
        '''
        command = input('please input command, type help to show the usage:\n').strip()
        return command

    def analysis(self, command):
        '''
        分析输入的命令，执行对应的操作。
        命令是一个以空格区分的字符串，因此需要使用split将命令切分成一个列表，第0个元素代表命令，后面的元素是参数。
        '''
        command_list = command.split(' ')
        if not command:
            return None
        keyword = command_list[0]
        if keyword in self.method_dict:
            para_dict = self.generate_para_dict(command_list[1:])
            #help 和exit是不需要参数的，因此要使用if 来将它们和其他的命令分开处理。
            self.method_dict[keyword](para_dict) if keyword not in ['help', 'exit'] else self.method_dict[keyword]()
        else:
            self.show_help()

    def show_help(self):
        help_message = '''
        the basic usage is like this:

        command [col_title1=info col_title2=info ...]
        for example:

        show
        show id=1
        show age=20 name=jike

        add id=8 name=kingname age=23 sex=male salary=9999999

        del id=3

        update id=2 name=kingname

        '''
        self.show_message(help_message)

    def show_message(self, message):
        print(message)

    def show_person_info(self, paras):
        '''
        show命令在不带参数的情况下，会显示所有人的信息。带了参数，就会根据参数来做过滤。
        '''
        if paras:
            self.show_spicific_person_info(paras)
        else:
            self.show_all_info()

    def show_all_info(self):
        all_person_info = self.col.find()
        self.generate_show_output(all_person_info)

    def show_spicific_person_info(self, para_dict):
        try:
            result = self.col.find(para_dict)
            self.generate_show_output(result)
        except Exception as e:
            output = 'query person info error, because: {}'.format(e)
            self.show_message(output)

    def add_person_info(self, para_dict):
        '''
        添加人员信息，由于id没有使用MongoDB的_id,所以需要自行判断是否重复。
        id是必需的信息，所以这个方法也会坚持添加的信息中是否有id
        '''
        def check_if_id_exists(person_id):
            '''
            笨办法遍历数据库，看新增的这个id是否已经存在，如果存在就返回False，不存在就返回True
            '''
            return True if [x for x in self.col.find({'id': person_id})] else False

        try:
            if set(para_dict.keys()) != set(self.COL_NAME_SET):
                print('info is incomplete! can not add to database.')
                return
        except Exception as e:
            print('the para_dict is invaild!')
            return

        if not para_dict or 'id' not in para_dict:
            print('everyone must have id!')
            return

        exi = check_if_id_exists(para_dict['id'])
        if exi:
            print('the id has already exists, please change to another one.')
            return
        try:
            self.col.insert(para_dict)
        except Exception as e:
            output = 'add person info error, because: {}'.format(e)
            self.show_message(output)

    def update_person_info(self, para_dict):
        '''
        这个方法用来更新人员信息。更新信息是根据id来查找的，因此id是必需的。
        '''
        if not para_dict or not 'id' in para_dict:
            print('please use id to identify person.')
            return
        try:
            for key, value in para_dict.items():
                if key == 'id':
                    person_id = value
                else:
                    col_name = key
                    new_value = value
            self.col.update_one({'id': person_id}, {'$set': {col_name: new_value}})
        except Exception as e:
            print('update person info error because: {}'.format(e))

    def del_person_info(self, para_dict):
        '''
        删除人员信息。
        '''
        if not para_dict:
            print('you have to identify who you want to delete.')
            return

        try:
            result = self.col.delete_many(para_dict)
            output = 'you have delete {} person(s)'.format(result.deleted_count)
        except Exception as e:
            output = 'delete person error, because: {}'.format(e)
        self.show_message(output)

    def generate_para_dict(self, paras):
        '''
        生成字典形式的参数，从而方便其他方法使用。
        paras是一个列表，包含了很多xx=yy这样格式的参数。这里用=做分割，左边的是key, 右边的是value
        '''
        para_dict = {}
        try:
            for para in paras:
                key, value = para.split('=')
                para_dict[key] = value
            return para_dict
        except Exception as e:
            print('the para error: {}'.format(e))

    def generate_show_output(self, query_result):
        '''
        输出查询的结果。限定了输出的内容只有id,name,age,sex,salary这几项，并且使用ljust, center和rjust来让
        格式显得比较整齐。
        '''
        output = 'id'.ljust(20) + \
                 'name'.ljust(20) + \
                 'age'.center(20) + \
                 'sex'.center(20) + \
                 'salary'.rjust(20) + '\n'

        for each_person in query_result:
            try:
                output += str(each_person['id']).ljust(20) + \
                          each_person['name'].ljust(20) + \
                          str(each_person['age']).center(20) + \
                          each_person['sex'].center(20) + \
                          str(each_person['salary']).rjust(20) + '\n'
            except Exception as e:
                print('generate output error because: {}'.format(e))
        self.show_message(output)

if __name__ == '__main__':
    database_manager = DataBaseManager()
