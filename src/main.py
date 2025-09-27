import argparse
from datetime import datetime
from .hybrid import recommend
from .contextual import Context
from .utils import print_df
from .notifications import generate_notifications


def main():
    parser = argparse.ArgumentParser(description="Smart Menu - Personalized Recommendations")
    parser.add_argument("--user", type=int, required=True, help="User ID")
    parser.add_argument("--budget", type=str, default=None, help="Budget level: low|mid|high")
    parser.add_argument("--time", type=str, default=None, help="Time of day: morning|lunch|afternoon|dinner")
    parser.add_argument("--top", type=int, default=10, help="Top K recommendations")
    args = parser.parse_args()

    ctx = Context(user_id=args.user, now=datetime.now(), budget_level=args.budget, time_of_day=args.time)
    recs = recommend(args.user, top_k=args.top, ctx=ctx)
    print_df(recs)
    print("\nNotifications:")
    for n in generate_notifications(args.user):
        print(f"- [{n['type']}] {n['title']}: {n['body']} -> {n['cta']}")


if __name__ == "__main__":
    main()


