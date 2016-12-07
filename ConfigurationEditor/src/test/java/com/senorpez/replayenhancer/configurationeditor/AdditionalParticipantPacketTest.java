package com.senorpez.replayenhancer.configurationeditor;

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

import static org.hamcrest.CoreMatchers.equalTo;
import static org.junit.Assert.assertThat;

public class AdditionalParticipantPacketTest {
    private final static Byte packetType = 2;
    private final static Byte offset = 16;
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
    private static AdditionalParticipantPacket packet;

    @Before
    public void setUp() throws Exception {
        ByteBuffer packetData = ByteBuffer.allocate(1028);

        packetData.putShort(Short.MAX_VALUE);
        packetData.put(packetType);
        packetData.put(offset);
        names.forEach(string -> packetData.put(Arrays.copyOf(string.getBytes(StandardCharsets.UTF_8), 64)));
        packetData.rewind();

        packet = new AdditionalParticipantPacket(packetData);
    }

    @Test
    public void getOffset() throws Exception {
        Integer expResult = offset.intValue();
        Integer result = packet.getOffset();
        assertThat(result, equalTo(expResult));
    }

    @Test
    public void readShort() throws Exception {
        ByteBuffer data = ByteBuffer.allocate(Short.BYTES).putShort(Short.MAX_VALUE);
        data.rewind();

        Short expResult = Short.MAX_VALUE;
        Short result = AdditionalParticipantPacket.ReadShort(data);
        assertThat(result, equalTo(expResult));
    }

    @Test
    public void readChar() throws Exception {
        ByteBuffer data = ByteBuffer.allocate(Byte.BYTES).put(Byte.MAX_VALUE);
        data.rewind();

        Integer expResult = (int) Byte.MAX_VALUE;
        Integer result = AdditionalParticipantPacket.ReadChar(data);
        assertThat(result, equalTo(expResult));
    }

    @Test
    public void readByte() throws Exception {
        ByteBuffer data = ByteBuffer.allocate(Byte.BYTES).put(Byte.MAX_VALUE);
        data.rewind();

        Integer expResult = (int) Byte.MAX_VALUE;
        Integer result = AdditionalParticipantPacket.ReadByte(data);
        assertThat(result, equalTo(expResult));
    }

    @Test
    public void readFloat() throws Exception {
        ByteBuffer data = ByteBuffer.allocate(Float.BYTES).putFloat(Float.MAX_VALUE);
        data.rewind();

        Float expResult = Float.MAX_VALUE;
        Float result = AdditionalParticipantPacket.ReadFloat(data);
        assertThat(result, equalTo(expResult));
    }

    @Test
    public void readString() throws Exception {
        String testString = "Lotus 98T";
        ByteBuffer data = ByteBuffer.allocate(testString.length()).put(testString.getBytes(StandardCharsets.UTF_8));
        data.rewind();

        String expResult = testString;
        String result = AdditionalParticipantPacket.ReadString(data, testString.length());
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
        Integer expResult = 2;
        Integer result = packet.getPacketType();
        assertThat(result, equalTo(expResult));
    }

    @Test
    public void getNames() throws Exception {
        Object[] expResult = names.toArray();
        ObservableList<SimpleStringProperty> result = packet.getNames();

        assertThat(result.stream().map(SimpleStringProperty::get).collect(Collectors.toList()),
                IsIterableContainingInOrder.contains(expResult));
    }
}
