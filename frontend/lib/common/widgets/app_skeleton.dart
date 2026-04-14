import 'package:flutter/material.dart';
import 'package:streetballer/common/constants/animations.dart';
import 'package:streetballer/common/constants/borders.dart';
import 'package:streetballer/common/constants/colors.dart';

class AppSkeleton extends StatefulWidget {
  final double width;
  final double height;
  final double borderRadius;

  const AppSkeleton({
    super.key,
    this.width = double.infinity,
    required this.height,
    this.borderRadius = borderRadiusSmall,
  });

  @override
  State<AppSkeleton> createState() => _AppSkeletonState();
}

class _AppSkeletonState extends State<AppSkeleton> with SingleTickerProviderStateMixin {
  late final AnimationController _controller;
  late final Animation<double> _opacity;

  @override
  void initState() {
    super.initState();
    _controller = AnimationController(vsync: this, duration: animationSlow)
      ..repeat(reverse: true);
    _opacity = Tween<double>(begin: 0.3, end: 0.8).animate(
      CurvedAnimation(parent: _controller, curve: animationCurve),
    );
  }

  @override
  void dispose() {
    _controller.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return FadeTransition(
      opacity: _opacity,
      child: Container(
        width: widget.width,
        height: widget.height,
        decoration: BoxDecoration(
          color: colorOutline,
          borderRadius: BorderRadius.circular(widget.borderRadius),
        ),
      ),
    );
  }
}
