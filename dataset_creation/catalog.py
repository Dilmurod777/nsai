import re


class GeneralCatalog:
    def Count(self, Objects):
        return str(len(Objects)) if Objects else None

    def Exists(self, Objects):
        return True if len(Objects) > 0 else False

    def Unique(self, Objects):
        if len(Objects) > 1:
            raise ValueError('unique() got len > 1')
        return Objects[0]

    def ExtractNumbers(self, Value):
        # re.findall(r"(\d+)", Value)
        return re.findall(r"\d+\.\d+|\d+", Value)

    def ExtractID(self, AttrID, Query):
        regex_dict = {
            'figure_id': r'[\d|-]+[A-Z]+$',
            'task_id': r'[\d-]+$',
            'subtask_id': r'[\d-]+$',
            'title': r'[\d-]+[A-Z]$'
        }
        return re.findall(regex_dict[AttrID], Query)[0]

    def NotUnderstood(self):
        reply = 'Request is not understood. Please, check the query.'
        return reply


class KnowledgeCatalog:
    def FilterAttr(self, Attr, AttrValue, DataObjects):
        result = []
        for data_object in DataObjects:
            if data_object[Attr] == AttrValue:
                result.append(data_object)
        return result

    def FilterType(self, Type, DataObjects):
        result = []
        for data_object in DataObjects:
            if Type in data_object.keys():
                result += data_object[Type]
        return result

    def QueryAttr(self, Attr, DataObject):
        try:
            return DataObject[Attr]
        except:
            return None

    def ShowInfo(self, DataObjects):
        result = ''
        if DataObjects is None:
            return result

        if type(DataObjects) is str:
            return DataObjects

        for DataObject in DataObjects:
            for k, d in DataObject.items():
                if type(d) == str:
                    result += ': '.join([k, str(d)]) + '\n'
                else:
                    result += ': '.join([k, str(len(d)) + ' item(s)']) + '\n'
        return result


class Actions3DCatalog:
    def CreateActions(self, action_type, reference_specified, numbers):
        actions = []
        reference_object = None
        if reference_specified == 'Yes':
            reference_object = numbers[-1]
            numbers = numbers[:-1]

        for number in numbers:
            action = {
                action_type: [number, reference_object]
            }
            actions.append(action)
        return actions

    def CheckActionsValidity(self, checking_actions, reference_actions):
        for i in range(len(checking_actions)):
            if checking_actions[i] != reference_actions[i]:
                return 'No'
        return 'Yes'

    def Detach(self, validity, actions):
        if validity == 'Yes':
            reply = 'Performing the following actions \n'
            for action in actions:
                reply += self.make_action_reply(action)
        else:
            reply = 'Please check validity of your request. You must follow the manual!'
        return reply.strip()

    def Attach(self, validity, actions):
        return self.Detach(validity, actions)

    def Filter3DAttr(self, attr, attr_value, root):
        result = []
        if attr == 'items':
            # print(root)
            return attr_value


        for data_object in root:
            if data_object[attr] == attr_value:
                result.append(data_object)
        return result

    def ShowSide(self, side, figure):
        return ' '.join(['showing', side, 'side', 'of figure', str(figure)])

    def Highlight(self, state, objects):
        reply = ''
        if state == 'on':
            reply = ' '.join(['Highlighting object(s)', str(objects)])
        else:
            reply = ' '.join(['Hiding highlights from object(s)', str(objects)])
        return reply

    def CloseLook(self, objects):
        reply = ' '.join(['Close Looking at object(s)', str(objects)])
        return reply

    def Scale(self, state, figure, ratio):
        reply = ' '.join(['Scaling', state, 'figure', figure['name'], 'by', str(ratio)])
        return reply

    def SideBySideLook(self, figure):
        reply = ' '.join(['Showing side by side look of objects in figure', figure['name']])
        return reply

    def Animate(self, state, figure):
        reply_dict = {
            'on': 'Animating',
            'off': 'Stopping animation of'
        }
        reply = ' '.join([reply_dict[state], 'figure', figure['name']])
        return reply

    def Visibility(self, state, objects):
        reply_dict = {
            'on': 'Showing',
            'off': 'Hiding'
        }
        if type(objects) is dict:
            objects = objects['name']
        reply = ' '.join([reply_dict[state], str(objects)])
        return reply

    def Reset(self, Object):
        reply = ' '.join(['Resetting', 'figure', Object['name']])
        return reply

    def ExecuteType(self, Type, Actions):
        reply_dict = {
            'tasks': 'task',
            'subtasks': 'subtask',
            'instructions': 'instruction'
        }
        reply = ' '.join(['Executing', reply_dict[Type], 'with actions:', str(Actions)])
        return reply

    def make_action_reply(self, action):
        reply = ''
        for key, items in action.items():
            prep = 'from' if key == 'detach' else 'to'
            reply += ' '.join([key, action[key][0], prep, action[key][1], '\n'])
        return reply

