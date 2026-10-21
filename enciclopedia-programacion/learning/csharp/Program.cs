using System;
using System.Collections.Generic;
class Program {
    static Dictionary<string, int> Totals((string Category, int Cents)[] entries) {
        var result = new Dictionary<string, int>();
        foreach (var entry in entries) {
            result.TryGetValue(entry.Category, out int previous);
            result[entry.Category] = checked(previous + entry.Cents);
        }
        return result;
    }
    static bool TryPositive(string text, out int value) {
        return int.TryParse(text, out value) && value > 0;
    }
    static bool Affordable(int balance, int price, int quantity) {
        if (balance < 0 || price < 0 || quantity < 0) return false;
        return (long)price * quantity <= balance;
    }
    static void Check(bool condition) {
        if (!condition) throw new Exception("test failed");
    }
    static void Main() {
        var result = Totals(new[] { ("food", 125), ("food", 75), ("bus", 100) });
        Check(result["food"] == 200 && result.Count == 2);
        Check(Totals(Array.Empty<(string, int)>()).Count == 0);
        Check(TryPositive("12", out int n) && n == 12);
        Check(!TryPositive("0", out _) && !TryPositive("abc", out _));
        Check(Affordable(500, 125, 4));
        Check(!Affordable(499, 125, 4));
        Check(!Affordable(int.MaxValue, int.MaxValue, 2));
        Check(!Affordable(-1, 1, 1));
        bool overflow = false;
        try { Totals(new[] { ("x", int.MaxValue), ("x", 1) }); }
        catch (OverflowException) { overflow = true; }
        Check(overflow);
        Console.WriteLine("csharp: OK");
    }
}
