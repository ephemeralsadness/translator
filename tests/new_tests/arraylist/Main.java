class Main {
    public static void main(String[] args) {
        Arraylist<Integer> v = new Arraylist<Integer>();

        for (int i = 0; i < 10; i += 1) {
            v.add(i);
        }
        for (int i = 0; i < 5; i += 1) {
            v.remove(0);
        }
        System.out.println(v.isEmpty());
        System.out.println(v.size());
        for (int i = 0; i < 5; i += 1) {
            System.out.print(v.get(i));
        }
        System.out.println(v.contains(8));

    }
}