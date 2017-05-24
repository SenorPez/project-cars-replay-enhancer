package com.senorpez.projectcars.replayenhancer;

import com.fasterxml.jackson.annotation.JsonProperty;
import io.swagger.annotations.Api;
import io.swagger.annotations.ApiOperation;
import io.swagger.annotations.ApiParam;
import org.springframework.hateoas.ResourceSupport;
import org.springframework.web.bind.annotation.*;

import java.util.List;
import java.util.concurrent.atomic.AtomicInteger;
import java.util.stream.Collectors;

import static org.springframework.hateoas.mvc.ControllerLinkBuilder.linkTo;
import static org.springframework.hateoas.mvc.ControllerLinkBuilder.methodOn;

@Api(tags = {"races"})
@RequestMapping(value = "/races", method = {RequestMethod.GET})
@ResponseBody
@RestController
class RaceController {
    class RaceList extends ResourceSupport {
        @JsonProperty("races")
        private final List<Race> raceList;

        RaceList() {
            AtomicInteger index = new AtomicInteger(0);
            raceList = Application.RACES.stream()
                    .map(race -> RaceController.addLink(index.getAndIncrement(), race))
                    .collect(Collectors.toList());
            this.add(linkTo(methodOn(RaceController.class).races()).withSelfRel());
        }
    }

    @ApiOperation(
            value = "Returns all races.",
            notes = "Returns all races in the dataset.",
            response = Race.class,
            responseContainer = "List"
    )
    @RequestMapping("")
    RaceList races() {
        return new RaceList();
    }

    @ApiOperation(
            value = "Returns a race.",
            notes = "Returns a race as specified by its ID number.",
            response = Race.class
    )
    @RequestMapping("/{raceId}")
    Race races(
            @ApiParam(
                    value = "ID of race to return",
                    required = true)
            @PathVariable Integer raceId) {
        if (raceId < Application.RACES.size()) {
            return Application.RACES.get(raceId);
        } else {
            throw new RaceNotFoundAPIException(raceId);
        }
    }

    private static Race addLink(int index, Race race) {
        race.removeLinks();
        race.add(linkTo(methodOn(RaceController.class).races(index)).withSelfRel());
        return race;
    }
}
