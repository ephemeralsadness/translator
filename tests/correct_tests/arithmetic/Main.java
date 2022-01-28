class Main {
    public static void main(String[] args) {
        int a = 21;
        a %= 5;
        float b = 3;
        float c = a/b;
        c -= 0.1;
        boolean d = true;
        c += d;
        c = Math.min(c, a)
        System.out.print(c);
    }
}