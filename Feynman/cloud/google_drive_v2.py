import time
import errno
from collections import defaultdict, namedtuple
from socket import error as SocketError

from googleapiclient.discovery import build

from Feynman.etc.util import get_logger
from Feynman.serialize import Pickle_serializer
from Feynman.algorithms.graph.bfs import bfs
from Feynman.algorithms.disjoint.union_find import get_parent, union_parent


class Google_drive_data():
    def __init__(self, data, root='0AGVYmV18tFTYUk9PVA', max_size=3):
        self._data = data
        self._edge_list = self._make_edge_list()
        self._max_size = max_size

        self.root = root
        self.all_dic = defaultdict(list)
        self.adj_dic = self._make_adj_dic()
        self.data_dic = self._make_data_dic()
        self.view_dic = defaultdict(list)
        self.remove_list = list()

        self._pruning_overlap_file(max_size=self._max_size)
        self._pruning_zombie_file()

    def _make_edge_list(self):
        EdgeList = namedtuple('listuple', 'child parent')
        edge_list = list()
        for d in self._data:
            child = d['id']
            for parent in d['parents']:
                edge_list.append(EdgeList(child=child, parent=parent))
        return edge_list

    def _make_adj_dic(self):
        adj_dic = defaultdict(list)
        for d in self._data:
            child = d['id']
            for parent in d['parents']:
                adj_dic[parent].append(child)
        return adj_dic

    def _make_data_dic(self):
        dic = defaultdict()
        for i, d in enumerate(self._data):
            child = d['id']
            for parent in d['parents']:
                dic[child] = d
        return dic

    def _pruning_overlap_file(self, max_size):
        for parent, children in bfs(self.adj_dic, self.root):
            qu = defaultdict(list)
            if not children:
                continue
            for child in children:
                qu[self.data_dic[child]['name']].append(child)
            for filename in qu.keys():
                qu[filename].sort(key=lambda x: self.data_dic[x]['createdTime'], reverse=True)
            for filename in qu.keys():
                self.remove_list += qu[filename][max_size:]
                self.view_dic[parent] += qu[filename][:max_size]

    def _pruning_zombie_file(self):
        dic = defaultdict(str)
        for child, parent in self._edge_list:
            union_parent(dic, parent, child)
        for child, _ in self._edge_list:
            if get_parent(dic, child) != child:
                self.all_dic[get_parent(dic, child)].append(child)
        for root in self.all_dic.keys():
            if root != self.root:
                self.remove_list += self.all_dic[root]


class Google_drive():
    def __init__(self, path='token.pickle'):
        self.logger = get_logger()
        self._ps = Pickle_serializer()
        self.creds = self._ps.load(path)

        while True:
            try:
                self.service = build('drive', 'v3', credentials=self.creds)
                self.logger.info('Google drive access...')
                break
            except SocketError as e:
                if e.errno != errno.ECONNRESET:
                    self.logger.info('Connection reset by peer...')
                    time.sleep(60)

    def update_list(self):
        data = self.service.files().list(fields='*').execute()['files']
        self._file_data = Google_drive_data(data)

    def empty_list(self, arg=None):
        if not self._file_data.remove_list:
            self.logger.info('there is no file')
            return 'There is no file'
        for _id in self._file_data.remove_list:
            self.service.files().delete(fileId=_id).execute()
            self.logger.info('Delete old file : {}'.format(_id))
        return 'Clear'
