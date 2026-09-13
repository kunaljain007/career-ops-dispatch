import os, sys, json, subprocess, urllib.request

POOL_FILE = os.path.join(os.path.dirname(__file__), 'data', 'github_accounts_pool.json')

def load_pool():
    if not os.path.exists(POOL_FILE):
        return []
    with open(POOL_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_pool(pool):
    with open(POOL_FILE, 'w', encoding='utf-8') as f:
        json.dump(pool, f, indent=2)


def perform_shift():
    pool = load_pool()
    if not pool:
        print("No accounts in pool!")
        return False

    active_idx = 0
    for i, acc in enumerate(pool):
        if acc.get('status') == 'active':
            active_idx = i
            break

    next_idx = (active_idx + 1) % len(pool)
    prev_acc = pool[active_idx]
    next_acc = pool[next_idx]

    print(f"[AUTO-SHIFT] Rotating from {prev_acc['username']} -> {next_acc['username']}...")

    pool[active_idx]['status'] = 'quota_exhausted'
    pool[next_idx]['status'] = 'active'
    save_pool(pool)

    new_url = f"https://{next_acc['token']}@github.com/{next_acc['username']}/{next_acc['repo']}.git"
    subprocess.run(['git', 'remote', 'set-url', 'origin', new_url], check=True)
    print(f"[AUTO-SHIFT] Updated remote origin. Pushing to {next_acc['username']}/ ...")
    subprocess.run(['git', 'push', 'origin', 'main:main'], check=False)
    subprocess.run(['git', 'push', 'origin', 'main:master'], check=False)
    print("[AUTO-SHIFT] Completed!")
    return True

if __name__ == '__main__':
    pool = load_pool()
    print(f"Accounts in pool: {len(pool)}")
    for acc in pool:
        print(f" - {acc['username']}: {acc.get('status')}")
    if len(sys.argv) > 1 and sys.argv[1] == '--shift':
        perform_shift()
    else:
        print("Run with --shift to trigger auto-shift to next account.")
