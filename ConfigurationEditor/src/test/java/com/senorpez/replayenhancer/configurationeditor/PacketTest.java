package com.senorpez.replayenhancer.configurationeditor;

import org.junit.Test;

import java.nio.ByteBuffer;

import static org.hamcrest.MatcherAssert.assertThat;
import static org.hamcrest.core.IsEqual.equalTo;

public class PacketTest {
    @Test
    public void readShort() throws Exception {
        ByteBuffer data = ByteBuffer.allocate(Short.BYTES).putShort(Short.MAX_VALUE);
        data.rewind();

        Short expResult = Short.MAX_VALUE;
        Short result = Packet.ReadShort(data);
        assertThat(result, equalTo(expResult));
    }

    @Test
    public void readChar() throws Exception {
        ByteBuffer data = ByteBuffer.allocate(Byte.BYTES).put(Byte.MAX_VALUE);
        data.rewind();

        Integer expResult = (int) Byte.MAX_VALUE;
        Integer result = Packet.ReadChar(data);
        assertThat(result, equalTo(expResult));
    }

    @Test
    public void readByte() throws Exception {
        ByteBuffer data = ByteBuffer.allocate(Byte.BYTES).put(Byte.MAX_VALUE);
        data.rewind();

        Integer expResult = (int) Byte.MAX_VALUE;
        Integer result = Packet.ReadByte(data);
        assertThat(result, equalTo(expResult));
    }

    @Test
    public void readFloat() throws Exception {
        ByteBuffer data = ByteBuffer.allocate(Float.BYTES).putFloat(Float.MAX_VALUE);
        data.rewind();

        Float expResult = Float.MAX_VALUE;
        Float result = Packet.ReadFloat(data);
        assertThat(result, equalTo(expResult));
    }

    @Test
    public void readString() throws Exception {
        String testString = "Lotus 98T";
        ByteBuffer data = ByteBuffer.allocate(testString.length()).put(testString.getBytes());
        data.rewind();

        String expResult = testString;
        String result = Packet.ReadString(data, testString.length());
        assertThat(result, equalTo(expResult));
    }
}