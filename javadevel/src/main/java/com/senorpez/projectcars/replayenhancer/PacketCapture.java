package com.senorpez.projectcars.replayenhancer;

import java.io.DataOutputStream;
import java.io.FileOutputStream;
import java.io.IOException;
import java.net.DatagramPacket;
import java.net.DatagramSocket;
import java.net.InetAddress;
import java.util.Arrays;
import java.util.concurrent.atomic.AtomicInteger;

public class PacketCapture {
    private static final AtomicInteger count = new AtomicInteger(0);

    public static void main(String[] args) throws IOException {
        try (DatagramSocket socket = new DatagramSocket(5606, InetAddress.getByName("0.0.0.0"));
            DataOutputStream outputStream = new DataOutputStream(new FileOutputStream("race1.replayenhancer"))) {
            while (true) {
                byte[] buf = new byte[2048];
                DatagramPacket packet = new DatagramPacket(buf, buf.length);
                socket.receive(packet);
                System.out.printf("Writing: %d\n", count.getAndIncrement());
                outputStream.writeShort(packet.getLength());
                outputStream.write(Arrays.copyOf(buf, packet.getLength()));
            }
        }
    }
}
