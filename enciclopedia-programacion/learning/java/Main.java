import java.util.HashMap;
import java.util.Map;

public class Main {
    static Map<String, Integer> count(String[] titles) {
        Map<String, Integer> result = new HashMap<>();
        for (String title : titles) {
            result.put(title, result.getOrDefault(title, 0) + 1);
        }
        return result;
    }
    static int available(Map<String, Integer> stock, String title) {
        return stock.getOrDefault(title, 0);
    }
    static void borrow(Map<String, Integer> stock, String title) {
        int units = available(stock, title);
        if (units <= 0) throw new IllegalArgumentException("unavailable");
        stock.put(title, units - 1);
    }
    static void check(boolean value) {
        if (!value) throw new AssertionError("test failed");
    }
    public static void main(String[] args) {
        Map<String, Integer> stock = count(new String[]{"A", "B", "A"});
        check(available(stock, "A") == 2);
        check(available(stock, "C") == 0);
        check(count(new String[]{}).isEmpty());
        borrow(stock, "A");
        check(available(stock, "A") == 1);
        boolean failed = false;
        try { borrow(stock, "C"); }
        catch (IllegalArgumentException e) { failed = true; }
        check(failed && !stock.containsKey("C"));
        System.out.println("java: OK");
    }
}
