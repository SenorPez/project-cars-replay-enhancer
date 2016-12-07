package com.senorpez.replayenhancer.configurationeditor;

import javafx.beans.property.SimpleIntegerProperty;
import org.junit.Before;
import org.junit.Test;

import static org.hamcrest.CoreMatchers.instanceOf;
import static org.hamcrest.core.IsEqual.equalTo;
import static org.junit.Assert.*;

public class PointStructureItemTest {
    private static final Integer points = 25;
    private static final Integer finishPosition = 1;
    private static PointStructureItem instance;

    @Before
    public void setUp() throws Exception {
        instance = new PointStructureItem(finishPosition, points);
    }

    @Test
    public void getPoints() throws Exception {
        Integer expResult = points;
        Integer result = instance.getPoints();
        assertThat(result, equalTo(expResult));
    }

    @Test
    public void setPoints() throws Exception {
        instance.setPoints(15);
    }

    @Test
    public void pointsProperty() throws Exception {
        SimpleIntegerProperty expResult = new SimpleIntegerProperty();
        SimpleIntegerProperty result = instance.pointsProperty();
        assertThat(result, instanceOf(expResult.getClass()));
    }

    @Test
    public void getFinishPosition() throws Exception {
        Integer expResult = finishPosition;
        Integer result = instance.getFinishPosition();
        assertThat(result, equalTo(expResult));
    }

    @Test
    public void setFinishPosition() throws Exception {
        instance.setFinishPosition(2);
    }

    @Test
    public void finishPositionProperty() throws Exception {
        SimpleIntegerProperty expResult = new SimpleIntegerProperty();
        SimpleIntegerProperty result = instance.finishPositionProperty();
        assertThat(result, instanceOf(expResult.getClass()));
    }
}
