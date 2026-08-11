-- Copyright (c) 2026 Akihisa Ono
-- SPDX-License-Identifier: MIT
-- RPOS-SOURCE-LANG: en

namespace RPOS

/-- Authority effects represented by the reusable responsibility-packet model.
This bounded model mirrors the public packet contract in which reusable packet
artifacts are evidence/coordination objects and cannot themselves grant or
restore execution authority. -/
inductive PacketAuthorityEffect where
  | none
  | grant
  deriving DecidableEq, Repr

/-- A reusable public responsibility packet is valid for the bounded model only
when its authority effect is explicitly `none`. -/
inductive ValidReusablePacket : PacketAuthorityEffect → Prop where
  | none : ValidReusablePacket .none

/-- INV-PACKET-001: a valid reusable responsibility packet cannot grant authority. -/
theorem valid_reusable_packet_cannot_grant_authority :
    ¬ ValidReusablePacket .grant := by
  intro h
  cases h

/-- INV-PACKET-002: every valid reusable responsibility packet has no authority effect. -/
theorem valid_reusable_packet_has_no_authority_effect {effect : PacketAuthorityEffect}
    (h : ValidReusablePacket effect) : effect = .none := by
  cases h
  rfl

end RPOS
