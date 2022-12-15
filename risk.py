import random

start_size = 1000
winrate = 0.55
bet = 0.15
max_bets = 1000
runs = 1000
end_sizes = []

for _ in range(runs):
    acc_size = start_size
    for _ in range(max_bets):
        if random.uniform(0, 1) > winrate:
            acc_size = acc_size * (1-bet)
        else:
            acc_size = acc_size * (1+bet)
    end_sizes.append(acc_size)

end_sizes.sort()
print(f'Min: {min(end_sizes)}')
print(f'Max: {max(end_sizes)}')
average = sum(end_sizes) / len(end_sizes)
print(f'Average: {average}')
median = end_sizes[int(runs/2)]
print(f'Median: {median}')
