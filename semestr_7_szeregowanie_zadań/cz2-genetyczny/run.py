import scheduler as sch

# 50 1 0.8

h = 0.2
k = 1
for n in [10]:
    s = sch.Scheduler(n, k, h)
    best_penalty = s.run_processing()
    print("n:{} k:{} h:{} -> {}".format(n, k, h, best_penalty))
