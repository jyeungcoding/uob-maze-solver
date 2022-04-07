#!/usr/bin/env python3
'''
This file contains a class for the PID controller system, including all memory elements
and functions needed to calculate the control signal. Initialise the class with the chosen
settings and the initial set point. Change the set point with new_setpoint(SetPoint); this
also resets the memory elements. update(ProcessVariable, TimeStep) outputs the control signal.
'''

# Import modules.
import numpy as np

class PID_Controller():

    def __init__(self, Kp, Ki, Kd, Ks, Kst, SetPoint, BufferSize, SaturationLimit, MinTheta):
        # SetPoint and SaturationLimit should be provided in a numpy vector, Size 2.
        if type(SetPoint) != np.ndarray:
            raise TypeError("SetPoint should be given in a size 2 numpy array.")
        elif SetPoint.shape != (2,):
            raise ValueError("SetPoint should be given in a size 2 numpy array.")

        self.Kp = Kp # Proportional coefficient.
        self.Ki = Ki # Integral coefficient.
        self.Kd = Kd # Derivative coefficient.
        self.Ks = Ks # Static boost coefficient.
        self.Kst = Kst # Static boost length coefficient. Higher numbers produce a shorter static boost.
        self.SetPoint = SetPoint # Current set point.
        self.BufferSize = BufferSize # Number of error values to store in the buffer.
        self.ErrorBuffer = np.zeros((9, self.BufferSize)) # Initialise error buffer (with additional rows for linear regression).
        self.BufferIteration = 0 # Record buffer iteration number.
        self.ErrorIntegral = np.array([0.0, 0.0]) # Initialise integrator.
        self.Calibrated = False # Initialise as not calibrated.
        self.ControlSignalCalibrated = np.array([0,0]) # Theta for zero tilt. Change after calibration.
        self.Saturation = np.array([False, False]) # Initialise saturation check.
        self.SaturationLimit = SaturationLimit # Control signal maximum angle limit.
        self.MinTheta = MinTheta # Minimum output theta.

    def __repr__(self):
        # Makes the class printable.
        return "PID Controller(Kp: %s, Ki: %s, Kd: %s, Set Point: %s)" % (self.Kp, self.Ki, self.Kd, self.SetPoint)

    def new_setpoint(self, SetPoint):
        self.SetPoint = SetPoint # Set new set point.
        self.ErrorIntegral = np.array([0.0, 0.0]) # Reset error integral.
        self.ErrorBuffer = np.zeros((9, self.BufferSize)) # Reset error buffer.
        self.BufferIteration = 0 # Reset buffer iteration number.

    def calibrate(self, ControlSignalCalibrated):
        # Theta for zero tilt. Change after calibration.
        self.ControlSignalCalibrated = ControlSignalCalibrated
        self.Calibrated = True
        self.reset()

    def reset(self):
        self.ErrorBuffer = np.zeros((9, self.BufferSize)) # Reset error buffer (with additional rows for linear regression).
        self.BufferIteration = 0 # Reset buffer iteration number.
        self.ErrorIntegral = np.array([0.0, 0.0]) # Reset integrator.
        self.Saturation = np.array([False, False]) # Reset saturation check.

    def error_buffer(self, ErrorValue, TimeStep):
        # Shifts error buffer by one and adds new error and timestep values.
        self.ErrorBuffer[0:3] = np.roll(self.ErrorBuffer[0:3], -1, 1) # Shifts error buffer to the left.
        self.ErrorBuffer[0:3, self.BufferSize - 1] = TimeStep + self.ErrorBuffer[0, self.BufferSize - 2], ErrorValue[0], ErrorValue[1] # Update rightmost values.
        self.BufferIteration += 1 # Update buffer iteration number.

    def conditional_integrator(self, ErrorValue, TimeStep):
        # Conditional integrator, clamps if ControlSignal is saturated and the error is the same sign as the integral.
        if np.all(self.Saturation) and int(np.sign(ErrorValue)[0]) == int(np.sign(self.ErrorIntegral)[0]) and int(np.sign(ErrorValue)[1]) == int(np.sign(self.ErrorIntegral)[1]):
            pass # X and Y clamped.
        elif self.Saturation[0] == False and self.Saturation[1] == True and int(np.sign(ErrorValue[1])) == int(np.sign(self.ErrorIntegral[1])):
            self.ErrorIntegral[0] += ErrorValue[0] * TimeStep # Y clamped.
        elif self.Saturation[0] == True and self.Saturation[1] == False and int(np.sign(ErrorValue[0])) == int(np.sign(self.ErrorIntegral[0])):
            self.ErrorIntegral[1] += ErrorValue[1] * TimeStep # X clamped.
        else:
            self.ErrorIntegral += ErrorValue * TimeStep # Both unclamped.
        return self.ErrorIntegral

    def linear_regression(self):
        '''
        Calculate derivative of error value using least squares linear regression method from a buffer of error value vs time.
        This is necessary as calculating instantaneous gradient from the noisy input signal from image detection would result
        in greatly incorrect derivative terms. Instead, calculating the average gradient of a buffer of error values effectively
        "filters" out the noise at the cost of a less accuracy and a slight lag.
        '''
        if self.BufferIteration >= self.BufferSize: # Only begin when buffer is full.
            MeanT = np.mean(self.ErrorBuffer[0]) # Calculate mean of T.
            MeanX = np.mean(self.ErrorBuffer[1]) # Calculate mean of X.
            MeanY = np.mean(self.ErrorBuffer[2]) # Calculate mean of Y.
            self.ErrorBuffer[3] = tuple(map(lambda T : T - MeanT, self.ErrorBuffer[0])) # Calculate T - MeanT.
            self.ErrorBuffer[4] = tuple(map(lambda x : x - MeanX, self.ErrorBuffer[1])) # Calculate x - MeanX.
            self.ErrorBuffer[5] = tuple(map(lambda y : y - MeanY, self.ErrorBuffer[2])) # Calculate y - MeanY.
            self.ErrorBuffer[6] = tuple(map(lambda T_MeanT, x_MeanX: T_MeanT * x_MeanX, self.ErrorBuffer[3], self.ErrorBuffer[4])) # Calculate T_MeanT * x_MeanX.
            self.ErrorBuffer[7] = tuple(map(lambda T_MeanT, y_MeanY: T_MeanT * y_MeanY, self.ErrorBuffer[3], self.ErrorBuffer[5])) # Calculate T_MeanT * y_MeanY.
            self.ErrorBuffer[8] = tuple(map(lambda T_MeanT: T_MeanT ** 2, self.ErrorBuffer[3])) # Calculate T_MeanT ^ 2.

            GradX = np.sum(self.ErrorBuffer[6]) / np.sum(self.ErrorBuffer[8]) # Gradient of x = (T_MeanT * x_MeanX) / (T_MeanT ^ 2).
            GradY = np.sum(self.ErrorBuffer[7]) / np.sum(self.ErrorBuffer[8]) # Gradient of y = (T_MeanT * y_MeanY) / (T_MeanT ^ 2).
            ErrorDerivative = np.array([GradX, GradY])
        else:
            ErrorDerivative = np.array([0.0, 0.0])
        return ErrorDerivative

    def static_boost(self, ThetaSignal, ErrorDerivative):
        if self.Calibrated == True: # Only apply static boost when the controller is calibrated.
            ThetaSignal = self.Ks * np.sign(ThetaSignal) * np.exp(-self.Kst * np.absolute(ErrorDerivative))
        return ThetaSignal

    def min_theta(self, ThetaSignal):
        # Apply minimum theta if necessary.
        if self.Calibrated == True: # Only apply minimum theta when the controller is calibrated.
            if ThetaSignal[0] > 0 and ThetaSignal[0] < self.MinTheta[0]:
                ThetaSignal[0] = self.MinTheta[0]
            elif ThetaSignal[0] < 0 and ThetaSignal[0] > -self.MinTheta[0]:
                ThetaSignal[0] = -self.MinTheta[0]
            if ThetaSignal[1] > 0 and ThetaSignal[1] < self.MinTheta[1]:
                ThetaSignal[1] = self.MinTheta[1]
            elif ThetaSignal[1] < 0 and ThetaSignal[1] > -self.MinTheta[1]:
                ThetaSignal[1] = -self.MinTheta[1]
        return ThetaSignal

    def gearing(self, ThetaSignal):
        # Convert theta to motor angle.
        ControlSignal = ThetaSignal * np.array([20 / 3, 10])
        return ControlSignal

    def saturation_clamp(self, ControlSignal):
        # Saturation clamp. Limits the ControlSignal to the SaturationLimit and records if saturation has occured.
        if ControlSignal[0] > self.SaturationLimit[0]:
            ControlSignal[0] = self.SaturationLimit[0]
            self.Saturation[0] = True
        elif ControlSignal[0] < -self.SaturationLimit[0]:
            ControlSignal[0] = -self.SaturationLimit[0]
            self.Saturation[0] = True
        else:
            self.Saturation[0] = False
        if ControlSignal[1] > self.SaturationLimit[1]:
            ControlSignal[1] = self.SaturationLimit[1]
            self.Saturation[1] = True
        elif ControlSignal[1] < -self.SaturationLimit[1]:
            ControlSignal[1] = -self.SaturationLimit[1]
            self.Saturation[1] = True
        else:
            self.Saturation[1] = False
        return ControlSignal

    def update(self, ProcessVariable, TimeStep):
        ErrorValue = self.SetPoint - ProcessVariable # Calculate error value.
        self.error_buffer(ErrorValue, TimeStep) # Update buffer.

        ErrorIntegral = self.conditional_integrator(ErrorValue, TimeStep) # Calculate integral value.
        ErrorDerivative = self.linear_regression() # Calculate derivative value.

        # Calculate PID terms and control signal.
        ProportionalTerm = self.Kp * ErrorValue
        IntegralTerm = self.Ki * ErrorIntegral
        DerivativeTerm = self.Kd * ErrorDerivative
        ThetaSignal = ProportionalTerm + IntegralTerm + DerivativeTerm # Calculate control signal.
        ThetaSignal = self.static_boost(ThetaSignal, ErrorDerivative) # Extra angle to help ball overcome static friction.
        ThetaSignal = self.min_theta(ThetaSignal) # Apply minimum theta if necessary.
        ControlSignal = self.gearing(ThetaSignal) # Convert theta to motor angle.
        ControlSignal += self.ControlSignalCalibrated # Apply calibrated level angles.
        ControlSignal = self.saturation_clamp(ControlSignal) # Apply saturation clamp if necessary.

        return ControlSignal, ProportionalTerm, IntegralTerm, DerivativeTerm

if __name__ == "__main__":
    import doctest
    doctest.testmod()
