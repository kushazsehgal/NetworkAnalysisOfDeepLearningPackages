# import os
import os

TOKEN = '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'
# TOKEN = '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'
# TOKEN = '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'
# TOKEN = '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'
# TOKEN = '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'
# TOKEN = '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'
res = os.system(f'curl -I -H "Authorization: token {TOKEN}" https://api.github.com')
# res2 = os.system(f'curl -H  "Authorization: token {TOKEN}" https://api.github.com/repos/scotthuang1989/image2tfrecords')
# print(res2)