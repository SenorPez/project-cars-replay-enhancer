package com.senorpez.replayenhancer.configurationeditor;

import javafx.beans.property.SimpleIntegerProperty;
import javafx.beans.property.SimpleObjectProperty;
import javafx.beans.property.SimpleStringProperty;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.junit.runners.Parameterized;

import java.util.Arrays;
import java.util.Collection;

import static org.hamcrest.CoreMatchers.instanceOf;
import static org.hamcrest.MatcherAssert.assertThat;
import static org.hamcrest.core.IsEqual.equalTo;
import static org.mockito.Mockito.mock;

@RunWith(Parameterized.class)
public class DriverTest {
    private final static String name = "Ayrton Senna";
    private final static String displayName = "Senna";
    private final static String shortName = "SEN";
    private final static String team = "Team Lotus";
    private final static Car car = mock(Car.class);
    private final static Integer points = 55;

    private Driver instance;
    private String expName;
    private String expDisplayName;
    private String expShortName;
    private Class expCar;
    private String expTeam;
    private Integer expPoints;

    @Parameterized.Parameters
    public static Collection<Object[]> data() {
        return Arrays.asList(new Object[][] {
                {new Driver(name), name, name, "A. Senna", Car.class, "", 0},
                {new Driver(displayName), displayName, displayName, displayName, Car.class, "", 0},
                {new Driver(name, displayName, shortName, car), name, displayName, shortName, Car.class, "", 0},
                {new Driver(name, displayName, shortName, car, team, points), name, displayName, shortName, Car.class, team, 55}
        });
    }

    public DriverTest(Driver driver, String name, String displayName, String shortName, Class car, String team, Integer points) {
        this.instance = driver;
        this.expName = name;
        this.expDisplayName = displayName;
        this.expShortName = shortName;
        this.expCar = car;
        this.expTeam = team;
        this.expPoints = points;
    }

    @Test
    public void getTeam() throws Exception {
        String expResult = expTeam;
        String result = instance.getTeam();
        assertThat(result, equalTo(expResult));
    }

    @Test
    public void setTeam() throws Exception {
        Driver instance = new Driver("New Driver");
        instance.setTeam("New Team");
    }

    @Test
    public void teamProperty() throws Exception {
        SimpleStringProperty expResult = new SimpleStringProperty();
        SimpleStringProperty result = instance.teamProperty();
        assertThat(result, instanceOf(expResult.getClass()));
    }

    @Test
    public void getShortName() throws Exception {
        String expResult = expShortName;
        String result = instance.getShortName();
        assertThat(result, equalTo(expResult));
    }

    @Test
    public void setShortName() throws Exception {
        Driver instance = new Driver("New Driver");
        instance.setShortName("New Short Name");
    }

    @Test
    public void shortNameProperty() throws Exception {
        SimpleStringProperty expResult = new SimpleStringProperty();
        SimpleStringProperty result = instance.shortNameProperty();
        assertThat(result, instanceOf(expResult.getClass()));
    }

    @Test
    public void getDisplayName() throws Exception {
        String expResult = expDisplayName;
        String result = instance.getDisplayName();
        assertThat(result, equalTo(expResult));
    }

    @Test
    public void setDisplayName() throws Exception {
        Driver instance = new Driver("New Driver");
        instance.setDisplayName("New Display Name");
    }

    @Test
    public void displayNameProperty() throws Exception {
        SimpleStringProperty expResult = new SimpleStringProperty();
        SimpleStringProperty result = instance.displayNameProperty();
        assertThat(result, instanceOf(expResult.getClass()));
    }

    @Test
    public void getName() throws Exception {
        String expResult = expName;
        String result = instance.getName();
        assertThat(result, equalTo(expResult));
    }

    @Test
    public void setName() throws Exception {
        Driver instance = new Driver("New Driver");
        instance.setName("New Name");
    }

    @Test
    public void nameProperty() throws Exception {
        SimpleStringProperty expResult = new SimpleStringProperty();
        SimpleStringProperty result = instance.nameProperty();
        assertThat(result, instanceOf(expResult.getClass()));
    }

    @Test
    public void getCar() throws Exception {
        Class expResult = expCar;
        Car result = instance.getCar();
        assertThat(result, instanceOf(expResult));
    }

    @Test
    public void setCar() throws Exception {
        Driver instance = new Driver("New Driver");
        instance.setCar(mock(Car.class));
    }

    @Test
    public void carProperty() throws Exception {
        SimpleObjectProperty<Car> expResult = new SimpleObjectProperty<>();
        SimpleObjectProperty<Car> result = instance.carProperty();
        assertThat(result, instanceOf(expResult.getClass()));
    }

    @Test
    public void getSeriesPoints() throws Exception {
        Integer expResult = expPoints;
        Integer result = instance.getSeriesPoints();
        assertThat(result, equalTo(expResult));
    }

    @Test
    public void setSeriesPoints() throws Exception {
        Driver instance = new Driver("New Driver");
        instance.setSeriesPoints(11);
    }

    @Test
    public void seriesPointsProperty() throws Exception {
        SimpleIntegerProperty expResult = new SimpleIntegerProperty();
        SimpleIntegerProperty result = instance.seriesPointsProperty();
        assertThat(result, instanceOf(expResult.getClass()));
    }
}
