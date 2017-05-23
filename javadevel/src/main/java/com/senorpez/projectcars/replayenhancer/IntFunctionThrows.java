package com.senorpez.projectcars.replayenhancer;

import java.io.IOException;
import java.util.function.IntFunction;

@FunctionalInterface
interface IntFunctionThrows<R> extends IntFunction<R> {
    @Override
    default R apply(int value) {
        try {
            applyThrows(value);
        } catch (final IOException e) {
            e.printStackTrace();
        }
        return null;
    }

    void applyThrows(int value) throws IOException;
}
