class Main {
    static void func(){
        int a = 1;
    }

    static float get_number_divided_by_two(float a){
        return a/2;
    }
    public static void main(String[] args) {
        func();
        int a = 15;
        a = get_number_divided_by_two(a);
        System.out.print(a);
    }
}