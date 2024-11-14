package org.example;

import javax.swing.*;
import javax.swing.border.BevelBorder;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.awt.event.KeyEvent;
import java.awt.event.KeyListener;
import java.util.Arrays;
import java.util.Random;

public class GameJFrame extends JFrame implements KeyListener, ActionListener {

    int[][] data = new int[4][4];
    int[][] win = new int[][] {
            {1, 2, 3, 4},
            {5, 6, 7, 8},
            {9, 10, 11, 12},
            {13, 14, 15, 0}
    };
    int x = 0;
    int y = 0;
    String path = "src/main/java/org/example/image/girl/girl1/";
    int count = 0;

    JMenuItem replayGame = new JMenuItem("replay game");
    JMenuItem reLogin = new JMenuItem("reLogin");
    JMenuItem exitGame = new JMenuItem("exit");
    JMenuItem qrCode = new JMenuItem("qrCode");

    public GameJFrame() {
        initJFrame();

        initMenuBar();

        initData();

        initImage();

        this.setVisible(true);
    }

    private void initData() {
        int[] tmpArr = {0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15};
        Random r = new Random();
        for (int i = 0; i < tmpArr.length; i++) {
            int index = r.nextInt(tmpArr.length);
            int temp = tmpArr[i];
            tmpArr[i] = tmpArr[index];
            tmpArr[index] = temp;
        }

        for (int i = 0; i < tmpArr.length; i++) {
            if (tmpArr[i] == 0) {
                x = i / 4;
                y = i % 4;
            }

            data[i / 4][i % 4] = tmpArr[i];

        }
    }

    private void initImage() {
        this.getContentPane().removeAll();

        if (Arrays.deepEquals(data, win)) {
            ImageIcon backGround = new ImageIcon("src/main/java/org/example/image/win.png");
            JLabel win = new JLabel(backGround);
            win.setBounds(400,400,197,73);
            this.getContentPane().add(win);
        }

        for (int i = 0; i <= 3 ; i++) {
            for (int j = 0; j <= 3; j++) {
                ImageIcon icon = new ImageIcon(path +
                        (data[i][j]) + ".jpg");
                JLabel jLabel = new JLabel(icon);
                jLabel.setBounds(105 * j + 43, 105 * i + 93,105,105);
                jLabel.setBorder(new BevelBorder(BevelBorder.RAISED));
                this.getContentPane().add(jLabel);
            }

        }

        ImageIcon backGround = new ImageIcon("src/main/java/org/example/image/background.png");
        JLabel bg = new JLabel(backGround);
        bg.setBounds(0,0,508,560);
        this.getContentPane().add(bg);

        JLabel countJLabel = new JLabel("count: " + count);
        countJLabel.setBounds(0, 600, 100, 20);
        this.getContentPane().add(countJLabel);


        this.getContentPane().repaint();
    }

    private void initMenuBar() {
        JMenuBar jMenuBar = new JMenuBar();
        JMenu functionJMenu = new JMenu("function");
        JMenu aboutJMenu = new JMenu("about");

        functionJMenu.add(replayGame);
        functionJMenu.add(reLogin);
        functionJMenu.add(exitGame);
        aboutJMenu.add(qrCode);

        jMenuBar.add(functionJMenu);
        jMenuBar.add(aboutJMenu);

        replayGame.addActionListener(this);
        reLogin.addActionListener(this);
        exitGame.addActionListener(this);

        this.setJMenuBar(jMenuBar);
    }

    private void initJFrame() {
        this.setSize(600, 800);
        this.setTitle("Title: puzzle game");
        this.setAlwaysOnTop(true);
        this.setLocationRelativeTo(null);
        this.setDefaultCloseOperation(EXIT_ON_CLOSE);
        this.setLayout(null);
        this.addKeyListener(this);
    }

    @Override
    public void keyTyped(KeyEvent e) {

    }

    @Override
    public void keyPressed(KeyEvent e) {
        int code = e.getKeyCode();
        if (code == 65) {
            this.getContentPane().removeAll();
            JLabel jLabel = new JLabel(new ImageIcon(path + "all.jpg"));
            jLabel.setBounds(43, 93, 420, 420);
            this.getContentPane().add(jLabel);
            ImageIcon backGround = new ImageIcon("src/main/java/org/example/image/background.png");
            JLabel bg = new JLabel(backGround);
            bg.setBounds(0,0,508,560);
            this.getContentPane().add(bg);
            this.getContentPane().repaint();
        }
    }

    @Override
    public void keyReleased(KeyEvent e) {
        if (Arrays.deepEquals(data, win)) return;
        int code = e.getKeyCode();
        switch (code) {
            case 37 -> {
                if (y == 3) return;
                data[x][y] = data[x][y + 1];
                data[x][y + 1] = 0;
                y++;
                count++;
            }
            case 38 -> {
                if (x == 3) return;
                data[x][y] = data[x + 1][y];
                data[x + 1][y] = 0;
                x++;
                count++;
            }
            case 39 -> {
                if (y == 0) return;
                data[x][y] = data[x][y - 1];
                data[x][y - 1] = 0;
                y--;
                count++;
            }
            case 40 -> {
                if (x == 0) return;
                data[x][y] = data[x - 1][y];
                data[x - 1][y] = 0;
                x--;
                count++;
            }
            case 87 ->
                data = win;
            default -> {
            }
        }
        initImage();
    }

    @Override
    public void actionPerformed(ActionEvent e) {
        Object event = e.getSource();
        if (event == replayGame) {
            initData();
            count = 0;
            initImage();
        } else if (event == reLogin) {
            this.setVisible(false);
            new LoginJFrame();
        } else if (event == exitGame) {
            System.exit(0);
        }
    }
}
