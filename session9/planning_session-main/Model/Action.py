from Model.Predicate import Predicate
from Model.State import State


class Action:
    def __init__(
        self,
        action_name: str,
        positive_preconditions: list[Predicate] | set[Predicate],
        negative_preconditions: list[Predicate] | set[Predicate],
        add_list: list[Predicate] | set[Predicate],
        delete_list: list[Predicate] | set[Predicate],
    ):
        self.action_name = action_name
        self.positive_preconditions = set(positive_preconditions)
        self.negative_preconditions = set(negative_preconditions)
        self.add_list = set(add_list)
        self.delete_list = set(delete_list)

    def is_relevant(self, state: State) -> bool:
        """
        STRIPS-style relevance:
        - اکشن حداقل یکی از goal های فعلی را تولید کند.
        - هیچ‌کدام از goal های فعلی را delete نکند.
        """
        # آیا اکشن حداقل یک literal از goal را اضافه می‌کند؟
        achieves_something = not self.add_list.isdisjoint(state.literals)

        # آیا اکشن goalهای فعلی را تخریب می‌کند؟
        harms_goal = not self.delete_list.isdisjoint(state.literals)

        return achieves_something and not harms_goal

    def regress(self, state: State) -> State:
        """
        Regression برای goal فعلی G با اکشن a:

        G' = (G − add(a)) ∪ pre(a)

        همه چیز positive است (فقط set از literals داریم).
        """
        new_goal_literals = (state.literals - self.add_list).union(
            self.positive_preconditions
        )

        # State جدید نشان‌دهندهٔ goal قبل از اجرای این اکشن است
        return State(self.action_name, list(new_goal_literals))

    def progress(self, state: State) -> State:
        """
        Forward execution (همون قبلی خودت)
        """
        result = state.literals.union(self.add_list) - self.delete_list
        return State(self.action_name, result)

    def is_applicable(self, state: State) -> bool:
        """
        اکشن وقتی قابل اجراست که:
        - تمام positive preconditions داخل state باشند.
        - هیچ‌کدام از negative preconditions داخل state نباشند.
        """
        is_applicable = (
            self.positive_preconditions.issubset(state.literals)
            and self.negative_preconditions.isdisjoint(state.literals)
        )
        return is_applicable

    def __str__(self) -> str:
        return (
            f"Action: {self.action_name}"
            + f"\nPositive preconditions: {self.positive_preconditions}"
            + f"\nNegative preconditions: {self.negative_preconditions}"
            + f"\nAdd list: {self.add_list}"
            + f"\nDelete list: {self.delete_list}\n"
        )

    def __repr__(self) -> str:
        return str(self)
