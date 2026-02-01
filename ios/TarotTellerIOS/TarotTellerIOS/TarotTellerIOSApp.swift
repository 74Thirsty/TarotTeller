import SwiftUI

@main
struct TarotTellerIOSApp: App {
    var body: some Scene {
        WindowGroup {
            ContentView()
        }
    }
}

                Spacer()

                Button(action: drawCard) {
                    Text("Draw a Card")
                        .font(.headline)
                        .frame(maxWidth: .infinity)
                        .padding()
                        .background(Color.blue)
                        .foregroundColor(.white)
                        .clipShape(RoundedRectangle(cornerRadius: 12, style: .continuous))
                }
            }
            .padding()
            .navigationTitle("TarotTeller")
        }
    }

    private func drawCard() {
        if let card = deck.randomElement() {
            selectedCard = card
            isReversed = Bool.random()
        }
    }
}