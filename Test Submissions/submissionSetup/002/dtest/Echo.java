import java.util.Scanner;
public class Echo{
    public static void main(String[] args) {
        System.out.println("Hello World");
        Scanner in = new Scanner(System.in);

        for(int i = 0; i < 5; i++){
            System.out.println(in.nextLine());
        }
        
        in.close();
    }
}