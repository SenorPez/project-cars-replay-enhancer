package com.senorpez.projectcars.replayenhancer;

import com.fasterxml.jackson.annotation.JsonProperty;

class RaceNotFoundAPIException extends APIException {
    @JsonProperty("status")
    private final Integer status = 404;
    @JsonProperty("code")
    private final String code;
    @JsonProperty("message")
    private final String messageApi;

    public RaceNotFoundAPIException(Integer raceId) {
        this.code = status.toString() + "-races-" + raceId;
        this.messageApi = String.format("Race with ID of %d not found.", raceId);
    }
}
