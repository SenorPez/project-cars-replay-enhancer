package com.senorpez.replayenhancer.configurationeditor;

import org.hamcrest.collection.IsIterableContainingInOrder;
import org.junit.After;
import org.junit.Before;
import org.junit.Test;

import java.nio.ByteBuffer;
import java.nio.charset.StandardCharsets;
import java.util.ArrayList;
import java.util.List;
import java.util.stream.Collectors;
import java.util.stream.IntStream;

import static org.hamcrest.CoreMatchers.equalTo;
import static org.junit.Assert.assertThat;

public class TelemetryDataPacketTest {
    private final static Byte packetType = 0;
    private final static Byte numParticipants = 11;

    private static List<TelemetryDataPacket> packets = new ArrayList<>(7);

    @Before
    public void setUp() throws Exception {

        for (byte i = 0; i < 7; i++) {
            ByteBuffer packetData = ByteBuffer.allocate(1367);

            packetData.putShort(Short.MAX_VALUE);
            packetData.put(packetType);

            packetData.put(Byte.MAX_VALUE);
            packetData.put(Byte.MAX_VALUE);

            packetData.put(numParticipants);

            packetData.put(Byte.MAX_VALUE);
            packetData.put(Byte.MAX_VALUE);
            packetData.put(Byte.MAX_VALUE);
            packetData.put(Byte.MAX_VALUE);

            packetData.put(i);
            packetData.rewind();

            packets.add(new TelemetryDataPacket(packetData));
        }
    }

    @After
    public void tearDown() throws Exception {
        packets.clear();
    }

    @Test
    public void getNumParticipants() throws Exception {
        List<Integer> expResult = IntStream.range(0, 7).map(number -> 11).boxed().collect(Collectors.toList());
        List<Integer> result = packets.stream().map(TelemetryDataPacket::getNumParticipants).collect(Collectors.toList());
        assertThat(result, IsIterableContainingInOrder.contains(expResult.toArray()));
    }

    @Test
    public void getRaceState() throws Exception {
        List<Integer> expResult = IntStream.range(0, 7).map(number -> number).boxed().collect(Collectors.toList());
        List<Integer> result = packets.stream().map(TelemetryDataPacket::getRaceState).collect(Collectors.toList());
        assertThat(result, IsIterableContainingInOrder.contains(expResult.toArray()));
    }

    @Test
    public void readShort() throws Exception {
        ByteBuffer data = ByteBuffer.allocate(Short.BYTES).putShort(Short.MAX_VALUE);
        data.rewind();

        Short expResult = Short.MAX_VALUE;
        Short result = TelemetryDataPacket.ReadShort(data);
        assertThat(result, equalTo(expResult));
    }

    @Test
    public void readChar() throws Exception {
        ByteBuffer data = ByteBuffer.allocate(Byte.BYTES).put(Byte.MAX_VALUE);
        data.rewind();

        Integer expResult = (int) Byte.MAX_VALUE;
        Integer result = TelemetryDataPacket.ReadChar(data);
        assertThat(result, equalTo(expResult));
    }

    @Test
    public void readByte() throws Exception {
        ByteBuffer data = ByteBuffer.allocate(Byte.BYTES).put(Byte.MAX_VALUE);
        data.rewind();

        Integer expResult = (int) Byte.MAX_VALUE;
        Integer result = TelemetryDataPacket.ReadByte(data);
        assertThat(result, equalTo(expResult));
    }

    @Test
    public void readFloat() throws Exception {
        ByteBuffer data = ByteBuffer.allocate(Float.BYTES).putFloat(Float.MAX_VALUE);
        data.rewind();

        Float expResult = Float.MAX_VALUE;
        Float result = TelemetryDataPacket.ReadFloat(data);
        assertThat(result, equalTo(expResult));
    }

    @Test
    public void readString() throws Exception {
        String testString = "Lotus 98T";
        ByteBuffer data = ByteBuffer.allocate(testString.length()).put(testString.getBytes(StandardCharsets.UTF_8));
        data.rewind();

        String expResult = testString;
        String result = TelemetryDataPacket.ReadString(data, testString.length());
        assertThat(result, equalTo(expResult));
    }

    @Test
    public void getBuildVersionNumber() throws Exception {
        List<Integer> expResult = IntStream.range(0, 7).map(number -> Short.MAX_VALUE).boxed().collect(Collectors.toList());
        List<Integer> result = packets.stream().map(TelemetryDataPacket::getBuildVersionNumber).collect(Collectors.toList());
        assertThat(result, IsIterableContainingInOrder.contains(expResult.toArray()));
    }

    @Test
    public void getPacketType() throws Exception {
        List<Integer> expResult = IntStream.range(0, 7).map(number -> 0).boxed().collect(Collectors.toList());
        List<Integer> result = packets.stream().map(TelemetryDataPacket::getPacketType).collect(Collectors.toList());
        assertThat(result, IsIterableContainingInOrder.contains(expResult.toArray()));
    }
}