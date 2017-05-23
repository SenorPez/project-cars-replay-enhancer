package com.senorpez.projectcars.replayenhancer;

import java.io.IOException;
import java.util.function.IntFunction;

@FunctionalInterface
public interface IntFunctionThrows<R> extends IntFunction<R> {

    @Override
    default R apply(int value) {
        try {
            return applyThrows(value);
        } catch (final IOException e) {
            e.printStackTrace();
        }
        return null;
    }

    R applyThrows(int value) throws IOException;
}
