from pymongo import MongoClient


class DataBaseManager(object):
    COL_NAME_SET = ['id', 'name', 'age', 'sex', 'salary']

    def __init__(self):
        client = MongoClient()
        database = client.people
        self.col = database.personal_info
        self.method_dict = {
            'add': self.add_person_info,
            'update': self.update_person_info,
            'del': self.del_person_info,
            'show': self.show_person_info,
            'help': self.show_help,
            'exit': exit
        }
        self.run()

    def run(self):
        '''
        启动一个循环, 直到输入exit为止
        拿到用户输入, 分析执行
        '''
        command = 'help'
        while command != 'exit':
            command = self.getInput()
            self.analysis(command)

    def analysis(self, command):

        '''
        分析具体是哪个命令, 执行对应操作

        '''
        if not command:
            return None
        '''
        以空格(1个以及以上)为间隔提取命令中的参数
        '''
        command_list = command.split()
        keyword = command_list[0]

        if keyword in self.method_dict:
            param_dict = self.generate_param_dict(command_list[1:])
            self.method_dict[keyword](param_dict) if keyword not in ['help', 'exit'] else self.method_dict[keyword]()
        else:
            self.show_help()

    def generate_param_dict(self, params):

        param_dict = {}

        #输入的命令是以空格为分割, 使用split切成列表, 第一个元素为键名, 第二个是value值
        try:
            for param in params:
                key, value = param.split('=')
                param_dict[key] = value

            return param_dict

        except Exception as e:
            print('tha param error: {}'.format(e))

    def getInput(self):
        command = input('please input command, type help to show the usage:\n').strip()
        return command

    def add_person_info(self, param_dict):
        '''
        添加人员, 如果id已存在或者信息不全就给出提示

        :param param_dict:
        :return:
        '''
        def check_if_id_exists(person_id):
            return True if [x for x in self.col.find({'id': person_id})] else False

        try:
            if set(param_dict.keys()) != set(self.COL_NAME_SET):
                print('info is incomplete! can not add to database.')
                return
        except  Exception as e:
            print('the param_dict is invalid!')
            return

        if check_if_id_exists(param_dict['id']):
            print('the id has already exists, please change to another one.')
            return
        try:
            self.col.insert(param_dict)
        except Exception as e:
            output = 'add person info error, because: {}'.format(e)
            print(output)

    def update_person_info(self, param_dict):

        '''
        使用id更新人员信息
        :param param_dict:
        :return:
        '''
        if not 'id' in param_dict:
            print('please use id to identify person.')
            return

        if len(param_dict.keys()) != 2:
            print('please update a single property each time')
            return

        try:
            for key, value in param_dict.items():
                if key == 'id':
                    person_id = value
                else:
                    col_name = key
                    new_value = value
            self.col.update_one({'id': person_id}, {'$set': {col_name: new_value}})
        except Exception as e:
            print('update person info error because: {}'.format(e))

    def del_person_info(self, param_dict):

        if not param_dict:
            print('you have to identify who you want to delete.')
            return

        try:
            result = self.col.delete_many(param_dict)
            output = 'you have delete {} person(s)'.format(result.deleted_count)
        except Exception as e:
            output = 'delete person error, because: {}'.format(e)
        print(output)

    def show_person_info(self, params):
        '''
        show 不带参数时显示所有的人员信息, 有的话根据条件过滤显示

        :param params:
        :return:
        '''
        if params:
            self.show_spicific_person_info(params)
        else:
            self.show_all_info()

    def show_all_info(self):

        all_person_info = self.col.find()
        self.generate_show_output(all_person_info)

    def show_spicific_person_info(self, param_dict):

        try:
            result = self.col.find(param_dict)
            self.generate_show_output(result)
        except Exception as e:
            output = 'query person info error, because: {}'.format(e)
            print(output)

    def generate_show_output(self, query_result):

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
        print(output)

    def show_help(self):
        '''
        help命令或者无用输入对应的输出信息

        :return:
        '''
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
        print(help_message)

if __name__ == '__main__':
    DataBaseManager()
