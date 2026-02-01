import SwiftUI

struct ContentView: View {
    var body: some View {
        TabView {
            DrawView()
                .tabItem {
                    Label("Draw", systemImage: "sparkles")
                }
            LibraryView(cards: TarotDeck.sample)
                .tabItem {
                    Label("Library", systemImage: "books.vertical")
                }
        }
    }
}

#Preview {
    ContentView()
}