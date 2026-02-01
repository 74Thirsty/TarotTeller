import SwiftUI

struct TarotCard: Identifiable {
    let id = UUID()
    let name: String
    let upright: String
    let reversed: String
}

struct ContentView: View {
    private let deck: [TarotCard] = [
        TarotCard(
            name: "The Magician",
            upright: "Focus your willpower and act with intention.",
            reversed: "Re-align your tools before moving ahead."
        ),
        TarotCard(
            name: "The High Priestess",
            upright: "Trust the wisdom that lives beneath the surface.",
            reversed: "Invite clarity before committing to a path."
        ),
        TarotCard(
            name: "The Sun",
            upright: "Lean into optimism and shared celebration.",
            reversed: "Let a small ritual restore your confidence."
        )
    ]

    @State private var selectedCard: TarotCard?
    @State private var isReversed = false

    var body: some View {
        NavigationStack {
            VStack(spacing: 24) {

                if let selectedCard {
                    Text(selectedCard.name)
                        .font(.title.bold())

                    Text(isReversed ? selectedCard.reversed : selectedCard.upright)
                        .font(.body)
                } else {
                    Text("Tap below to draw your first card.")
                }

                Spacer()

                Button("Draw a Card", action: drawCard)
                    .font(.headline)
                    .frame(maxWidth: .infinity)
                    .padding()
                    .background(Color.blue)
                    .foregroundColor(.white)
                    .clipShape(RoundedRectangle(cornerRadius: 12))
            }
            .padding()
            .navigationTitle("TarotTeller")
        }
    }

    private func drawCard() {
        selectedCard = deck.randomElement()
        isReversed = Bool.random()
    }
}
