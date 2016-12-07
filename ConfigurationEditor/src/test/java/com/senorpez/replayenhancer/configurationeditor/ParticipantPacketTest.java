package com.senorpez.replayenhancer.configurationeditor;

import javafx.beans.property.SimpleFloatProperty;
import javafx.beans.property.SimpleStringProperty;
import javafx.collections.ObservableList;
import org.hamcrest.collection.IsIterableContainingInOrder;
import org.junit.Before;
import org.junit.Test;

import java.nio.ByteBuffer;
import java.nio.charset.StandardCharsets;
import java.util.Arrays;
import java.util.List;
import java.util.stream.Collectors;

import static org.hamcrest.core.IsEqual.equalTo;
import static org.junit.Assert.assertThat;

public class ParticipantPacketTest {
    private final static Byte packetType = 1;
    private final static String carName = "Lotus 98T";
    private final static String carClass = "Vintage F1 C";
    private final static String trackLocation = "Monaco";
    private final static String trackVariation = "GP";

    private final static List<String> names = Arrays.asList(
            "Nico Rosberg",
            "Lewis Hamilton",
            "Daniel Ricciardo",
            "Sebastian Vettel",
            "Kimi Räikkönen",
            "Max Verstappen",
            "Sergio Perez",
            "Valtteri Bottas",
            "Nico Hulkenberg",
            "Fernando Alonso",
            "Felipe Massa",
            "Carlos Sainz",
            "Romain Grosjean",
            "Daniil Kvyat",
            "Jenson Button",
            "Kevin Magnussen");

    private final static List<Float> fastestLaps = Arrays.asList(
            77.939F,
            78.005F,
            78.294F,
            78.446F,
            78.519F,
            78.763F,
            79.131F,
            79.170F,
            79.213F,
            79.223F,
            79.232F,
            79.670F,
            79.868F,
            80.219F,
            80.372F,
            81.342F
    );

    private static ParticipantPacket packet;

    @Before
    public void setUp() throws Exception {
        ByteBuffer packetData = ByteBuffer.allocate(1347);

        packetData.putShort(Short.MAX_VALUE);
        packetData.put(packetType);
        packetData.put(Arrays.copyOf(carName.getBytes(StandardCharsets.UTF_8), 64));
        packetData.put(Arrays.copyOf(carClass.getBytes(StandardCharsets.UTF_8), 64));
        packetData.put(Arrays.copyOf(trackLocation.getBytes(StandardCharsets.UTF_8), 64));
        packetData.put(Arrays.copyOf(trackVariation.getBytes(StandardCharsets.UTF_8), 64));

        names.forEach(string -> packetData.put(Arrays.copyOf(string.getBytes(StandardCharsets.UTF_8), 64)));

        fastestLaps.forEach(packetData::putFloat);

        packetData.rewind();
        packet = new ParticipantPacket(packetData);
    }

    @Test
    public void getCarName() throws Exception {
        String expResult = carName;
        String result = packet.getCarName();
        assertThat(result, equalTo(expResult));
    }

    @Test
    public void getCarClass() throws Exception {
        String expResult = carClass;
        String result = packet.getCarClass();
        assertThat(result, equalTo(expResult));
    }

    @Test
    public void getTrackLocation() throws Exception {
        String expResult = trackLocation;
        String result = packet.getTrackLocation();
        assertThat(result, equalTo(expResult));
    }

    @Test
    public void getTrackVariation() throws Exception {
        String expResult = trackVariation;
        String result = packet.getTrackVariation();
        assertThat(result, equalTo(expResult));
    }

    @Test
    public void getNames() throws Exception {
        Object[] expResult = names.toArray();
        ObservableList<SimpleStringProperty> result = packet.getNames();

        assertThat(result.stream().map(SimpleStringProperty::get).collect(Collectors.toList()),
                IsIterableContainingInOrder.contains(expResult));
    }

    @Test
    public void getFastestLapTimes() throws Exception {
        Object[] expResult = fastestLaps.toArray();
        ObservableList<SimpleFloatProperty> result = packet.getFastestLapTimes();

        assertThat(result.stream().map(SimpleFloatProperty::get).collect(Collectors.toList()),
                IsIterableContainingInOrder.contains(expResult));
    }

    @Test
    public void readShort() throws Exception {
        ByteBuffer data = ByteBuffer.allocate(Short.BYTES).putShort(Short.MAX_VALUE);
        data.rewind();

        Short expResult = Short.MAX_VALUE;
        Short result = ParticipantPacket.ReadShort(data);
        assertThat(result, equalTo(expResult));
    }

    @Test
    public void readChar() throws Exception {
        ByteBuffer data = ByteBuffer.allocate(Byte.BYTES).put(Byte.MAX_VALUE);
        data.rewind();

        Integer expResult = (int) Byte.MAX_VALUE;
        Integer result = ParticipantPacket.ReadChar(data);
        assertThat(result, equalTo(expResult));
    }

    @Test
    public void readByte() throws Exception {
        ByteBuffer data = ByteBuffer.allocate(Byte.BYTES).put(Byte.MAX_VALUE);
        data.rewind();

        Integer expResult = (int) Byte.MAX_VALUE;
        Integer result = ParticipantPacket.ReadByte(data);
        assertThat(result, equalTo(expResult));
    }

    @Test
    public void readFloat() throws Exception {
        ByteBuffer data = ByteBuffer.allocate(Float.BYTES).putFloat(Float.MAX_VALUE);
        data.rewind();

        Float expResult = Float.MAX_VALUE;
        Float result = ParticipantPacket.ReadFloat(data);
        assertThat(result, equalTo(expResult));
    }

    @Test
    public void readString() throws Exception {
        String testString = "Lotus 98T";
        ByteBuffer data = ByteBuffer.allocate(testString.length()).put(testString.getBytes(StandardCharsets.UTF_8));
        data.rewind();

        String expResult = testString;
        String result = ParticipantPacket.ReadString(data, testString.length());
        assertThat(result, equalTo(expResult));
    }

    @Test
    public void getBuildVersionNumber() throws Exception {
        Integer expResult = (int) Short.MAX_VALUE;
        Integer result = packet.getBuildVersionNumber();
        assertThat(result, equalTo(expResult));
    }

    @Test
    public void getPacketType() throws Exception {
        Integer expResult = 1;
        Integer result = packet.getPacketType();
        assertThat(result, equalTo(expResult));
    }
}
