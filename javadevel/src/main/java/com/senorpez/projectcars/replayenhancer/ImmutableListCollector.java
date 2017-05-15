package com.senorpez.projectcars.replayenhancer;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;
import java.util.function.Supplier;
import java.util.stream.Collector;

class ImmutableListCollector {
    private static <T, A extends List<T>> Collector<T, A, List<T>> toImmutableList(Supplier<A> collectionFactory) {
        return Collector.of(
                collectionFactory,
                List::add,
                (left, right) -> {
                    left.addAll(right);
                    return left;
                },
                Collections::unmodifiableList);
    }

    static <T> Collector<T, List<T>, List<T>> toImmutableList() {
        return toImmutableList(ArrayList::new);
    }
}
