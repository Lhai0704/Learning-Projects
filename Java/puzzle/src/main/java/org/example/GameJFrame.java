package org.example;

import javax.swing.*;

public class GameJFrame extends JFrame {

    public GameJFrame() {
        initJFrame();

        initMenuBar();


        this.setVisible(true);
    }

    private void initMenuBar() {
        JMenuBar jMenuBar = new JMenuBar();
        JMenu functionJMenu = new JMenu("function");
        JMenu aboutJMenu = new JMenu("about");
        JMenuItem replayGame = new JMenuItem("replay game");
        JMenuItem reLogin = new JMenuItem("reLogin");
        JMenuItem exitGame = new JMenuItem("exit");
        JMenuItem qrCode = new JMenuItem("qrCode");

        functionJMenu.add(replayGame);
        functionJMenu.add(reLogin);
        functionJMenu.add(exitGame);
        aboutJMenu.add(qrCode);

        jMenuBar.add(functionJMenu);
        jMenuBar.add(aboutJMenu);

        this.setJMenuBar(jMenuBar);
    }

    private void initJFrame() {
        this.setSize(600, 800);
        this.setTitle("Title: puzzle game");
        this.setAlwaysOnTop(true);
        this.setLocationRelativeTo(null);
        this.setDefaultCloseOperation(EXIT_ON_CLOSE);
    }
}
