package com.senorpez.projectcars.replayenhancer;

import org.springframework.http.HttpStatus;
import org.springframework.web.bind.annotation.RestControllerAdvice;

@RestControllerAdvice
class APIExceptionHandlers extends BaseAPIExceptionHandler {
    public APIExceptionHandlers() {
        registerMapping(RaceNotFoundAPIException.class, "RACE_NOT_FOUND", "Race not found.", HttpStatus.NOT_FOUND);
    }
}
