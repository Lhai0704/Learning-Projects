package org.example;

public class User {
    private String name;
    private String password;
    private String idCard;
    private String phone;

    public User() {
    }

    public User(String name, String password, String idCard, String phone) {
        this.name = name;
        this.password = password;
        this.idCard = idCard;
        this.phone = phone;
    }

    public String getName() {
        return name;
    }

    public void setName(String name) {
        this.name = name;
    }

    public String getPassword() {
        return password;
    }

    public void setPassword(String password) {
        this.password = password;
    }

    public String getIdCard() {
        return idCard;
    }

    public void setIdCard(String idCard) {
        this.idCard = idCard;
    }

    public String getPhone() {
        return phone;
    }

    public void setPhone(String phone) {
        this.phone = phone;
    }
}
