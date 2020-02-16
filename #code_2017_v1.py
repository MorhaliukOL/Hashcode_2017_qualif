import time
START = time.time()
VERSION = 1

NAME = "endpoint"
ENDPOINTDICT = {"datacenter": 0}
BASE_DICT = {}

files = ['me_at_the_zoo.in', 'kittens.in', 'videos_worth_spreading.in', 'trending_today.in']
filename = files[1]


def read_requests(requests):
    # endpoints = {'endpoint0': {video0: request0, video1: request1, ...}
    endpoints = {}
    for _ in range(requests):
        video, endpoint, request = list(map(int, f.readline().split()))
        if endpoints.get(endpoint, False):
            # Check if endpoint asked the video before
            if endpoints[endpoint].get(video):
                endpoints[endpoint][video] += request
            else:
                endpoints[endpoint].update({video: request})
        else:
            endpoints[endpoint] = {video: request}
    return endpoints


with open('input_data/' + filename) as f:
    # 1
    videos, endpoints, requests, CACHES, CACHES_SIZE = map(int, f.readline().split())

    # 2
    videos_lst = []
    for video in list(map(int, f.readline().split())):
        videos_lst.append(video)
    # videos_lst = [size_vid_1, size_vid_2, ...]

    # 3
    for endpoint_id in range(endpoints):
        datacenter_latency, caches_conn = list(map(int, f.readline().split()))
        BASE_DICT[endpoint_id] = ENDPOINTDICT.copy()
        BASE_DICT[endpoint_id]['datacenter'] = datacenter_latency
        if endpoints > 1:      # why do we need it ???
            for cache in range(caches_conn):
                cache_id, latency = list(map(int, f.readline().split()))
                BASE_DICT[endpoint_id][cache_id] = latency

    endp_data = read_requests(requests)
    #BASE_DICT = {enpoint_id: {'cache_id': latency, ... ,{'datacenter': latency}}


# caches_we_use = {cache_idx:[space, video0, video3], ...}
caches_we_use = {idx: [CACHES_SIZE] for idx in range(CACHES)}
for endpoint, requests in endp_data.items():
    ordered_req = sorted(requests.items(), key=lambda x: x[1], reverse=True)
    # cache_latency_dictionary
    c_l_dict = BASE_DICT[endpoint]
    cache_ord_by_latency = sorted(c_l_dict.items(), key=lambda x: x[1])[:-1]

    for vid_id, num_req in ordered_req:
        for cache_id, latency in cache_ord_by_latency:
            # check if there is enough space in the cache
            if caches_we_use[cache_id][0] >= videos_lst[vid_id]:
                caches_we_use[cache_id].append(vid_id)
                caches_we_use[cache_id][0] -= videos_lst[vid_id]

num_caches = sum([1 for idx in range(CACHES) if caches_we_use[idx][0] < 100])
cache_videos = [' '.join(map(str, [idx] + caches_we_use[idx][1:])) for idx in range(CACHES)]
cache_videos.insert(0, str(num_caches))
result = '\n'.join(cache_videos)

ex_time = time.time() - START

with open(f"output/{filename}_{ex_time:.5f}_v{VERSION}.txt", 'w') as file:
    file.writelines(result)

